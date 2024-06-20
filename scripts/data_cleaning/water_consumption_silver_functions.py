from datetime import datetime
import pandas as pd
import numpy as np


COLUMN_MAPPING = {
    'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'total_precip_mm',
    'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'station_pressure_mb',
    'PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)': 'max_pressure_last_hour_mb',
    'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)': 'min_pressure_last_hour_mb',
    'RADIACAO GLOBAL (Kj/m²)': 'global_radiation_kj_m2',
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'air_temp_c',
    'TEMPERATURA DO PONTO DE ORVALHO (°C)': 'dew_point_temp_c',
    'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)': 'max_temp_last_hour_c',
    'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)': 'min_temp_last_hour_c',
    'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)': 'max_dew_point_last_hour_c',
    'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)': 'min_dew_point_last_hour_c',
    'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)': 'max_humidity_last_hour_percentage',
    'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)': 'min_humidity_last_hour_percentage',
    'UMIDADE RELATIVA DO AR, HORARIA (%)': 'relative_humidity_percentage',
    'VENTO, DIREÇÃO HORARIA (gr) (° (gr))': 'wind_direction_deg',
    'VENTO, RAJADA MAXIMA (m/s)': 'max_wind_gust_m_s',
    'VENTO, VELOCIDADE HORARIA (m/s)': 'wind_speed_m_s'
}


def set_up(input_df):
    df = input_df.copy()
    df = df.rename(columns={
            "DATA/HORA": "timestamp",
            "VAZÃO ENTRADA (L/S)": "input_flow_rate",
            "NÍVEL RESERVATÓRIO (%)": "reservoir_level_percentage",
            "PRESSÃO (mca)": "pressure",
            "GMB 1 (10 OFF/ 90 ON)": "pump_1",
            "GMB 2(10 OFF/ 90 ON)": "pump_2",
        }).replace({
        "pump_1": {10: 0, 90: 1},
        "pump_2": {10: 0, 90: 1}
    })
    
    return df


def impute_faulty_data(input_df):
    df = input_df.copy()
    faulty_rows = df[df.reservoir_level_percentage == 0.0]

    for index, row in faulty_rows.iterrows():
        t_minus_1 = df.loc[:index-1, 'reservoir_level_percentage'].replace(0.0, pd.NA).last_valid_index()
        t_plus_1 = df.loc[index+1:, 'reservoir_level_percentage'].replace(0.0, pd.NA).first_valid_index()
        
        if pd.notna(t_minus_1) and pd.notna(t_plus_1):
            prev_level = df.at[t_minus_1, 'reservoir_level_percentage']
            next_level = df.at[t_plus_1, 'reservoir_level_percentage']
            imputed_level = round((prev_level + next_level) / 2, 2)
            df.at[index, 'reservoir_level_percentage'] = imputed_level
            
            prev_flow = df.at[t_minus_1, 'input_flow_rate']
            next_flow = df.at[t_plus_1, 'input_flow_rate']
            imputed_flow = round((prev_flow + next_flow) / 2, 2)
            df.at[index, 'input_flow_rate'] = imputed_flow

    return df


def fill_missing_pressure(input_df):
    df = input_df.copy()
    df.pressure = df.pressure.replace(0.0, np.nan)
    df.pressure = df.pressure.fillna(df.pressure.rolling(window=10, min_periods=1).mean())
    df.pressure = df.pressure.fillna(df.pressure.mean())
    df.pressure = df.pressure.round(2)
    
    return df


def fix_pump_status(input_df):
    df = input_df.copy()
    invalid_pump_rows = df[(df.pump_1 == 0) & (df.pump_2 == 0) & (df.input_flow_rate > 0)]

    for index, _ in invalid_pump_rows.iterrows():
        df.at[index, 'pump_2'] = 1

    return df


def fix_input_flow_rate(input_df):

    df = input_df.copy()
    invalid_rows = df[(df.input_flow_rate == 0) & ((df.pump_1 == 1) | (df.pump_2 == 1))]

    for index, row in invalid_rows.iterrows():
        df.at[index, 'input_flow_rate'] = df[df.input_flow_rate > 0].input_flow_rate.mean()
        
    return df


def create_necessary_columns(input_df):
    df = input_df.copy()
    df['reservoir_level_liters'] = df['reservoir_level_percentage'] * 1_000_000 / 100
    df['time_passed_seconds'] = df['timestamp'].diff().dt.total_seconds()
    df['total_liters_entered'] = df['input_flow_rate'] * df['time_passed_seconds']
    df['effective_liters_entered'] = df['reservoir_level_liters'].diff()
    df['total_liters_out'] = df['total_liters_entered'] - df['effective_liters_entered']
    df['output_flow_rate'] = df['total_liters_out'] / df['time_passed_seconds']
    df.loc[df['effective_liters_entered'] < 0, 'effective_liters_entered'] = 0
    df = df.drop(0)
    
    return df


def adjust_flow_rates(input_df):
    df = input_df.copy()
    problem_rows = df[df['total_liters_entered'] < df['effective_liters_entered']]
    
    for index, _ in problem_rows.iterrows():
        df.at[index, 'input_flow_rate'] = df.at[index, 'effective_liters_entered'] / df.at[index, 'time_passed_seconds']
        df.at[index, 'total_liters_entered'] = df.at[index, 'effective_liters_entered']
        df.at[index, 'total_liters_out'] = 0
        df.at[index, 'output_flow_rate'] = 0
    
    return df


def create_date_columns(input_df):
    df = input_df.copy()
    df['minute'] = df['timestamp'].dt.minute
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day
    df['day_of_week'] = df['timestamp'].dt.weekday
    df['week_of_year'] = df['timestamp'].dt.isocalendar().week
    df['month'] = df['timestamp'].dt.month
    df['year'] = df['timestamp'].dt.year
    
    return df


def fix_df(input_df):
    df = input_df.copy()
    df = set_up(df)
    df = impute_faulty_data(df)
    df = fill_missing_pressure(df)
    df = fix_pump_status(df)
    df = fix_input_flow_rate(df)
    df = create_necessary_columns(df)
    df = adjust_flow_rates(df)
    df = create_date_columns(df)
    df = df[[
        'timestamp', 'minute', 'hour', 'day', 'day_of_week', 'week_of_year', 'year', 'month',
        'input_flow_rate', 'reservoir_level_percentage', 'pressure', 'output_flow_rate',
        'pump_1', 'pump_2'
    ]]
    
    df = df.round(2).reset_index(drop=True)
    return df


def preprocess_weather_dataset(input_df):
    df = input_df.copy()
    df.drop(df.columns[-1], axis=1, inplace=True) 
    df['Hora UTC'] = df['Hora UTC'].apply(lambda x: datetime.strptime(x, '%H%M %Z')) 
    df['Data'] = pd.to_datetime(df['Data'], format='%Y/%m/%d')
    df['hour'] = df['Hora UTC'].dt.hour
    df['day'] = df['Data'].dt.day
    df['month'] = df['Data'].dt.month
    df['year'] = df['Data'].dt.year
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    df.drop(columns=['Data', 'Hora UTC'], axis=1, inplace=True)
    
    df = df[[
        "hour", "day", "month", "year", "relative_humidity_percentage", 
        "max_temp_last_hour_c", "min_temp_last_hour_c", "air_temp_c", 
        "total_precip_mm"
    ]]

    return df


def create_weather_dataset(df23, df24):
    df23 = preprocess_weather_dataset(df23)
    df24 = preprocess_weather_dataset(df24)
    df_23_24_concat = pd.concat([df23, df24], axis=0)
    return df_23_24_concat


def fill_na_with_moving_average(input_df, window=10):
    df = input_df.copy()
    
    for column in df.columns:
        if df[column].isna().sum() > 0:
            df[column] = df[column].transform(lambda x: x.fillna(x.rolling(window, min_periods=1).mean()))
            df[column] = df[column].ffill()
            df[column] = df[column].bfill()
        
    return df


def create_combined_dataset(input_df, input_weather_df, input_weather_complementary_df):
    df = input_df.copy()
    weather_df = input_weather_df.copy()
    merged_df = df.merge(weather_df, on=['hour', 'day', 'year', 'month'], how='left')
    comp_data = preprocess_weather_dataset(input_weather_complementary_df)
    merged_df = merged_df.sort_values(by=['day', 'month', 'hour', 'year'])
    comp_data = comp_data.sort_values(by=['day', 'month', 'hour', 'year'])
    merged_df_indexed = merged_df.set_index(['day', 'month', 'hour', 'year'])
    comp_data_indexed = comp_data.set_index(['day', 'month', 'hour', 'year'])
    merged_df_indexed.update(comp_data_indexed)
    full_df = merged_df_indexed.reset_index()
    filled_df = fill_na_with_moving_average(full_df)
    filled_df.sort_values(by='timestamp', inplace=True)
    filled_df = filled_df[[
        "timestamp", "minute", "hour", "day_of_week", "week_of_year", "year",
        "input_flow_rate", "reservoir_level_percentage", "pressure", "output_flow_rate",
        "pump_1", "pump_2", "air_temp_c", "total_precip_mm", "relative_humidity_percentage",
    ]]
    
    return filled_df


def calculate_time_diff(df):
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    return df


def calculate_pump_durations(df):
    df['pump_1_duration'] = df['pump_1'] * df['time_diff']
    df['pump_2_duration'] = df['pump_2'] * df['time_diff']
    return df


def resample_hourly(df):
    df_hourly = df.resample('h').agg({
        'minute': 'first',  # We will drop this column later
        'hour': 'first',
        'day_of_week': 'first',
        'week_of_year': 'first',
        'year': 'first',
        'input_flow_rate': 'mean',
        'reservoir_level_percentage': 'first',  # Use the first value of the hour
        'pressure': 'mean',
        'output_flow_rate': 'mean',
        'pump_1_duration': 'sum',  # Sum the durations
        'pump_2_duration': 'sum',  # Sum the durations
        'air_temp_c': 'mean',
        'total_precip_mm': 'sum',
        'relative_humidity_percentage': 'mean'
    })
    return df_hourly


def convert_pump_durations_to_percentage(df_hourly):
    seconds_in_hour = 3600
    df_hourly['pump_1'] = (df_hourly['pump_1_duration'] / seconds_in_hour).clip(0, 1)
    df_hourly['pump_2'] = (df_hourly['pump_2_duration'] / seconds_in_hour).clip(0, 1)
    return df_hourly


def fill_missing_values(df_hourly):
    df_hourly.ffill(inplace=True)
    df_hourly.bfill(inplace=True)
    return df_hourly


def prepare_final_dataframe(df_hourly):
    df_hourly.drop(columns=['minute', 'pump_1_duration', 'pump_2_duration'], inplace=True)
    df_hourly.reset_index(inplace=True)
    df_hourly['hour'] = df_hourly.hour.astype('int')
    df_hourly['day_of_week'] = df_hourly.day_of_week.astype('int')
    df_hourly['week_of_year'] = df_hourly.week_of_year.astype('int')
    df_hourly['year'] = df_hourly.year.astype('int')
    df_hourly = df_hourly.round(2)
    return df_hourly


def identify_and_adjust_anomalies(df_hourly):
    anomalies_increase = df_hourly[(df_hourly['input_flow_rate'] < df_hourly['output_flow_rate']) & (-df_hourly['reservoir_level_percentage'].diff(-1) > 0)]
    df_hourly.loc[anomalies_increase.index, 'input_flow_rate'] = df_hourly.loc[anomalies_increase.index, 'output_flow_rate'] + 0.01
    anomalies_decrease = df_hourly[(df_hourly['input_flow_rate'] > df_hourly['output_flow_rate']) & (-df_hourly['reservoir_level_percentage'].diff(-1) < 0)]
    df_hourly.loc[anomalies_decrease.index, 'output_flow_rate'] = df_hourly.loc[anomalies_decrease.index, 'input_flow_rate'] - 0.01
    
    return df_hourly


def add_missing_hours(df_hourly):
    full_range = pd.date_range(start=df_hourly['timestamp'].min(), end=df_hourly['timestamp'].max(), freq='h')
    df_hourly = df_hourly.set_index('timestamp').reindex(full_range).reset_index().rename(columns={'index': 'timestamp'})
    df_hourly['input_flow_rate'] = df_hourly['input_flow_rate'].ffill().bfill()
    df_hourly['output_flow_rate'] = df_hourly['output_flow_rate'].ffill().bfill()
    df_hourly['reservoir_level_percentage'] = df_hourly['reservoir_level_percentage'].ffill().bfill()
    added_rows = df_hourly['input_flow_rate'].isnull()
    df_hourly.loc[added_rows, 'input_flow_rate'] = df_hourly.loc[added_rows, 'output_flow_rate']
    
    return df_hourly


def create_hourly_df(input_df):
    df = input_df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = calculate_time_diff(df)
    df = calculate_pump_durations(df)
    df.set_index('timestamp', inplace=True)
    df_hourly = resample_hourly(df)
    df_hourly = convert_pump_durations_to_percentage(df_hourly)
    df_hourly = fill_missing_values(df_hourly)
    df_hourly = prepare_final_dataframe(df_hourly)
    df_hourly = identify_and_adjust_anomalies(df_hourly)
    df_hourly = add_missing_hours(df_hourly)
    return df_hourly
