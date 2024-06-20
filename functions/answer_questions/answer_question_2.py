import pandas as pd
import os

def get_average_flow_out_across_day():
    df = pd.read_parquet(os.path.join(os.path.dirname(__file__),"../../data/silver/water_consumption_silver.parquet"))
    
    df_weekdays = df[df['weekday'] < 5]
    df_weekends = df[df['weekday'] >= 5]

    flow_out_weekdays = df_weekdays.groupby('hour')['output_flow_rate'].mean().reset_index().rename(columns={'output_flow_rate': 'avg_weekday_output_flow'})
    flow_out_weekends = df_weekends.groupby('hour')['output_flow_rate'].mean().reset_index().rename(columns={'output_flow_rate': 'avg_weekend_output_flow'})
    
    df_combined = pd.merge(flow_out_weekdays, flow_out_weekends, on='hour', how='outer')
    df_combined.to_parquet(os.path.join(os.path.dirname(__file__),"../../data/gold/question_2_answer.parquet"))