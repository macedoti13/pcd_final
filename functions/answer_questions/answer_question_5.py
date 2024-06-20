import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
from answer_question_4_and_7 import forecast_next_24_hours_output_flow_rate
import pandas as pd

def simulate_empyting_reservoir(year, month, day, hour, return_df=True):
    original_input_df = pd.read_parquet(os.path.join(os.path.dirname(__file__),"../../data/silver/water_consumption_silver.parquet")) 
    input_df = original_input_df[original_input_df["timestamp"] == pd.Timestamp(year=year, month=month, day=day, hour=hour)]
    start_index = input_df.index.values.tolist()[0]
    yesterday_df = original_input_df.iloc[start_index-24:start_index, :].copy()
    forecast_df = forecast_next_24_hours_output_flow_rate(year, month, day, hour, save_df=False).rename(columns={'forecasted_output_flow_rate': 'output_flow_rate'})
    concated_df = pd.concat([input_df[['timestamp', 'reservoir_level_percentage', 'output_flow_rate']], forecast_df[['timestamp', 'output_flow_rate']]], axis=0)
    concated_df['total_liters_out'] = concated_df['output_flow_rate'] * 3600
    concated_df['percentage_out'] = concated_df['total_liters_out'] / 10000

    while concated_df['reservoir_level_percentage'].isnull().any():
        concated_df['reservoir_level_percentage'] = concated_df['reservoir_level_percentage'].fillna(concated_df['reservoir_level_percentage'].shift(1) - concated_df['percentage_out'])
        
    concated_df = concated_df.reset_index(drop=True)
    hours_until_empyting = concated_df[concated_df.reservoir_level_percentage < 0].index.tolist()[0]
    concated_df = concated_df.iloc[0:hours_until_empyting+1, :3]
    concated_df.loc[:, 'simulation'] = True
    yesterday_df.loc[:, 'simulation'] = False
    concated_df = pd.concat([yesterday_df[['timestamp', 'reservoir_level_percentage', 'output_flow_rate', 'simulation']], concated_df], axis=0).reset_index(drop=True)
    if return_df: 
        return concated_df
    concated_df.to_parquet(os.path.join(os.path.dirname(__file__),"../../data/gold/question_5_answer.parquet"))
    return hours_until_empyting