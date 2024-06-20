from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from xgboost import XGBRegressor
import numpy as np
import pickle

from utils import non_weather_training_columns_list



### Aqui ta errado!!!
def create_training_samples(df, with_weather, target):
    
    if with_weather:
        X = np.array(df.drop(columns=[target]))
    else: 
        columns_to_drop = non_weather_training_columns_list + [target]
        X = np.array(df.drop(columns=columns_to_drop))
        
    y = np.array(df[target])
    
    return X, y


def set_model_training_pipeline():
    model = XGBRegressor(learning_rate=0.01, early_stopping_rounds=100)
    cv = TimeSeriesSplit(n_splits=5)
    params = {"n_estimators": [100, 500, 1000, 5000], "max_depth": [3, 5, 10, 14], "learning_rate": [0.01, 0.05, 0.1]}
    clf = GridSearchCV(estimator=model, param_grid=params, cv=cv, scoring="neg_mean_absolute_error", n_jobs=-1, verbose=2)
    return clf


def train_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=100)
    return model.best_estimator_


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
