import pandas as pd

def create_lag_features(input_df):
    df = input_df.copy()
    
    features = []
    weather_features = []
    
    for lag in [1, 2, 3, 6, 12, 24]:  # You can choose the number of lags you need
        df[f'input_flow_rate_lag_{lag}'] = df['input_flow_rate'].shift(lag)
        df[f'reservoir_level_percentage_lag_{lag}'] = df['reservoir_level_percentage'].shift(lag)
        df[f'pressure_lag_{lag}'] = df['pressure'].shift(lag)
        df[f'output_flow_rate_lag_{lag}'] = df['output_flow_rate'].shift(lag)
        df[f'air_temp_c_lag_{lag}'] = df['air_temp_c'].shift(lag)
        df[f'total_precip_mm_lag_{lag}'] = df['total_precip_mm'].shift(lag)
        df[f'relative_humidity_percentage_lag_{lag}'] = df['relative_humidity_percentage'].shift(lag)
        df[f'pump_1_lag_{lag}'] = df['pump_1'].shift(lag)
        df[f'pump_2_lag_{lag}'] = df['pump_2'].shift(lag)
        
        features.extend([f'input_flow_rate_lag_{lag}', f'reservoir_level_percentage_lag_{lag}', f'pressure_lag_{lag}', 
                        f'output_flow_rate_lag_{lag}', f'pump_1_lag_{lag}', f'pump_2_lag_{lag}'])
        weather_features.extend([f'air_temp_c_lag_{lag}', f'total_precip_mm_lag_{lag}', f'relative_humidity_percentage_lag_{lag}'])
        
    return df, features, weather_features


def create_window_features(input_df):
    df = input_df.copy()

    features = []
    weather_features = []
    
    for window in [3, 6, 12, 24]:  
        df[f'input_flow_rate_roll_mean_{window}'] = df['input_flow_rate'].rolling(window=window).mean()
        df[f'reservoir_level_percentage_roll_mean_{window}'] = df['reservoir_level_percentage'].rolling(window=window).mean()
        df[f'pressure_roll_mean_{window}'] = df['pressure'].rolling(window=window).mean()
        df[f'output_flow_rate_roll_mean_{window}'] = df['output_flow_rate'].rolling(window=window).mean()
        df[f'air_temp_c_roll_mean_{window}'] = df['air_temp_c'].rolling(window=window).mean()
        df[f'total_precip_mm_roll_mean_{window}'] = df['total_precip_mm'].rolling(window=window).mean()
        df[f'relative_humidity_percentage_roll_mean_{window}'] = df['relative_humidity_percentage'].rolling(window=window).mean()
        df[f'pump_1_roll_mean_{window}'] = df['pump_1'].rolling(window=window).mean()
        df[f'pump_2_roll_mean_{window}'] = df['pump_2'].rolling(window=window).mean()
        
        features.extend([f'input_flow_rate_roll_mean_{window}', f'reservoir_level_percentage_roll_mean_{window}', 
                        f'pressure_roll_mean_{window}', f'output_flow_rate_roll_mean_{window}', f'pump_1_roll_mean_{window}',
                        f'pump_2_roll_mean_{window}'])
        weather_features.extend([f'air_temp_c_roll_mean_{window}', f'total_precip_mm_roll_mean_{window}', f'relative_humidity_percentage_roll_mean_{window}'])
        
    return df, features, weather_features


def create_targets(input_df):
    df = input_df.copy()
    
    targets = []
    for i in range(1, 25):  # 24 future time steps
        df[f'target_{i}'] = df['output_flow_rate'].shift(-i)
        targets.append(f'target_{i}')
        
    return df, targets


def create_training_dataset(input_df):
    df = input_df.copy()
    
    df, lag_features, weather_lag_features = create_lag_features(df)
    df, window_features, weather_window_features = create_window_features(df)
    df, targets = create_targets(df)
    df.dropna(inplace=True)
    
    date_features = ['timestamp', 'hour', 'day_of_week', 'week_of_year', 'year']
    all_lag_features = lag_features + weather_lag_features
    all_window_features = window_features + weather_window_features
    all_features = all_lag_features + all_window_features + date_features
    all_training_columns = all_features + targets
    
    return df[all_training_columns].reset_index(drop=True)
