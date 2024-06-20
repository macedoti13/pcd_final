from utils import non_weather_training_columns_list, with_weather_training_columns_list
import pandas as pd
import pickle


def forecast_next_24_hours_output_flow_rate(input_df, year, month, day, hour):
    
    timestamp = pd.Timestamp(year=year, month=month, day=day, hour=hour)
    input_df = input_df[input_df["timestamp"] == timestamp]
    
    X = input_df[non_weather_training_columns_list]
    X_weather = input_df[with_weather_training_columns_list]
    
    predictions = []
    for i in range(1, 25):
        new_prediction = {}
        next_timestamp = timestamp + pd.Timedelta(hours=i)
        model = pickle.load(open(f"../models/xgb_{i}h.pkl", "rb")) # aqui tem que mudar, esse path vai dar erro
        new_prediction['timestamp'] = next_timestamp
        new_prediction['forecasted_output_flow_rate'] = round(float(model.predict(X)[0]), 2)
        predictions.append(new_prediction)


    weather_predictions = []
    for i in range(1, 25):
        new_prediction = {}
        next_timestamp = timestamp + pd.Timedelta(hours=i)
        model = pickle.load(open(f"../models/xgb_with_weather_{i}h.pkl", "rb")) # aqui tem que mudar, esse path vai dar erro
        new_prediction['timestamp'] = next_timestamp
        new_prediction['weather_forecasted_output_flow_rate'] = round(float(model.predict(X_weather)[0]), 2)
        weather_predictions.append(new_prediction)
        
    predictions = pd.DataFrame(predictions)
    weather_predictions = pd.DataFrame(weather_predictions)
    merged_df = pd.merge(predictions, weather_predictions, on='timestamp')
        
    
    return merged_df