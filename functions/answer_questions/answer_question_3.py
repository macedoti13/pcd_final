import pandas as pd
import os

def get_avg_use_per_bomb_in_minutes_corrected() -> pd.DataFrame:
    df = pd.read_parquet(os.path.join(os.path.dirname(__file__),"../../data/silver/water_consumption_silver.parquet"))

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    peak_hours = (df["hour"] >= 18) & (df["hour"] <= 21)
    df["is_peak_hour"] = peak_hours
    df['pump_1_duration'] = df['pump_1'] * 3600
    df['pump_2_duration'] = df['pump_2'] * 3600
    
    daily_peak_usage = df[df['is_peak_hour']].groupby('date').agg({'pump_1_duration': 'sum', 'pump_2_duration': 'sum'})
    daily_off_peak_usage = df[~df['is_peak_hour']].groupby('date').agg({'pump_1_duration': 'sum', 'pump_2_duration': 'sum'})
    gmb_1_peak_avg = daily_peak_usage['pump_1_duration'].mean() / 60  
    gmb_1_off_peak_avg = daily_off_peak_usage['pump_1_duration'].mean() / 60  
    gmb_2_peak_avg = daily_peak_usage['pump_2_duration'].mean() / 60 
    gmb_2_off_peak_avg = daily_off_peak_usage['pump_2_duration'].mean() / 60  
    
    def convert_to_hours_and_minutes(minutes):
        if pd.isna(minutes):
            return "0 hours and 0 minutes"
        total_minutes = int(minutes)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours} hours and {minutes} minutes"
    
    data = {
        'pump': ['pump_1', 'pump_2'],
        'average_time_used_peak_hours': [
            convert_to_hours_and_minutes(gmb_1_peak_avg), 
            convert_to_hours_and_minutes(gmb_2_peak_avg)
        ],
        'average_time_used_offpeak_hours': [
            convert_to_hours_and_minutes(gmb_1_off_peak_avg), 
            convert_to_hours_and_minutes(gmb_2_off_peak_avg)
        ]
    }
    
    result_df = pd.DataFrame(data)
    result_df.to_parquet(os.path.join(os.path.dirname(__file__),"../../data/gold/question_3_answer.parquet"))