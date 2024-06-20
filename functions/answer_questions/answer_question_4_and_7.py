from utils import non_weather_training_columns_list, with_weather_training_columns_list
import pandas as pd
import pickle
import os

def forecast_next_24_hours_output_flow_rate(year, month, day, hour, save_df=True):
    
    input_df = pd.read_parquet(os.path.join(os.path.dirname(__file__),"../../data/silver/training_dataset.parquet"))
    timestamp = pd.Timestamp(year=year, month=month, day=day, hour=hour)
    input_df = input_df[input_df["timestamp"] == timestamp]
    
    X = input_df[non_weather_training_columns_list]
    X_weather = input_df[with_weather_training_columns_list]
    
    predictions = []
    for i in range(1, 25):
        new_prediction = {}
        next_timestamp = timestamp + pd.Timedelta(hours=i)
        model = pickle.load(open(os.path.join(os.path.dirname(__file__), f"../../models/xgb_{i}h.pkl", "rb")))
        new_prediction['timestamp'] = next_timestamp
        new_prediction['forecasted_output_flow_rate'] = round(float(model.predict(X)[0]), 2)
        predictions.append(new_prediction)


    weather_predictions = []
    for i in range(1, 25):
        new_prediction = {}
        next_timestamp = timestamp + pd.Timedelta(hours=i)
        model = pickle.load(open(os.path.join(os.path.dirname(__file__),f"../../models/xgb_with_weather_{i}h.pkl", "rb"))) 
        new_prediction['timestamp'] = next_timestamp
        new_prediction['weather_forecasted_output_flow_rate'] = round(float(model.predict(X_weather)[0]), 2)
        weather_predictions.append(new_prediction)
        
    predictions = pd.DataFrame(predictions)
    weather_predictions = pd.DataFrame(weather_predictions)
    merged_df = pd.merge(predictions, weather_predictions, on='timestamp')
    
    if not save_df:
        return merged_df
    merged_df.to_parquet(os.path.join(os.path.dirname(__file__),"../../data/gold/question_4_and_7_answer.parquet"))