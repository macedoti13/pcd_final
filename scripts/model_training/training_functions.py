from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from xgboost import XGBRegressor
import numpy as np
import pickle

from utils import non_weather_training_columns_list, with_weather_training_columns_list


def create_training_samples(df, with_weather, target):
    
    targets = []
    for i in range(1, 25):
        targets.append(f"target_{i}")
        
    if with_weather:
        X = np.array(df[with_weather_training_columns_list])
    else:
        X = np.array(df[non_weather_training_columns_list])
        
    y = np.array(df[target])
    
    return X, y


def set_model_training_pipeline():
    model = XGBRegressor() 
    params = {
        "n_estimators": [200, 300, 500, 1000],
        "max_depth": [3, 4, 5, 6, 10, 15],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "subsample": [0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.7, 0.8, 0.9, 1.0]
    }
    clf = RandomizedSearchCV(
        estimator=model,
        param_distributions=params,
        scoring="neg_mean_absolute_error",
        n_iter=50,  
        cv=3,  
        n_jobs=-1,
        verbose=2,
        random_state=42
    )
    return XGBRegressor(n_estimators=100, max_depth=1, learning_rate=0.01)


def train_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=100)
    return model


def train_xgb_model(df, with_weather, target):
    
    print(f"\nTraining model! with_weather: {with_weather}")
    
    # split the data
    train_df = df[df.year==2023]
    test_df = df[df.year==2024]
    
    # create the training samples
    X_train, y_train = create_training_samples(train_df, with_weather, target)
    X_test, y_test = create_training_samples(test_df, with_weather, target)
    
    # set the model training pipeline
    model = set_model_training_pipeline()
    
    # train the model
    model = train_model(model, X_train, y_train, X_test, y_test)
    
    return model
    
    
def save_model(model, path):
    pickle.dump(model, open(path, "wb"))
    
    
def calculate_error(y_test: np.ndarray, y_pred: np.ndarray):
    mae = round(mean_absolute_error(y_true=y_test, y_pred=y_pred), 2)
    mse = round(mean_squared_error(y_true=y_test, y_pred=y_pred), 2)
    rmse = round(np.sqrt(mse), 2)
    r2 = round(r2_score(y_true=y_test, y_pred=y_pred), 2)
    return mae, mse, rmse, r2

    
def print_error(model, df, with_weather):
        
    # split the data
    test_df = df[df.year==2024]
    
    # create the training samples
    X_test, y_test = create_training_samples(test_df, with_weather=with_weather, target='target_1')
    
    # predict
    y_pred = model.predict(X_test)
    
    # calculate the error
    mae, mse, rmse, r2 = calculate_error(y_test, y_pred)
    
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {rmse}")
    print(f"R2 Score: {r2}")
