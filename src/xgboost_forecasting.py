# Importing required libraries
import pandas as pd
import yfinance as yf
import pickle
import warnings
from datetime import date, timedelta
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor


# Creating a class XgBoost
class XgBoost:

    # Creating a constructor to initialize attributes
    def __init__(self, crop):

        # Initializing the crop
        self.crop = crop


    # Creating a function to load data
    def load_data(self):

        # Ignoring the warnings
        warnings.filterwarnings("ignore")

        # Defining the crop symbols
        crop_symbols = {
            "corn" : "ZC=F",
            "wheat" : "ZW=F",
            "soybeans" : "ZS=F"
        }

        # Retrieving the current date
        curr_date = date.today().strftime("%Y-%m-%d")

        # Loading the data
        df = yf.download(tickers=crop_symbols[self.crop.strip().lower()], start='2020-01-01', end=curr_date, progress=False)

        # Adding the index as a separate column
        df["Date"] = df.index

        # Resetting the index
        df = df.reset_index(drop=True)

        # Creating a new dataframe with the date and closing price
        new_df = df.loc[:,["Date", "Close"]]

        # Flattening the cloumns to make it a single-index column
        new_df.columns = ['Date' if col[0] == 'Date' else col[0] for col in new_df.columns]

        # Returning the final dataframe
        return new_df
    

    # Creating a function to train
    def train(self):

        # Loading the data
        df = self.load_data()

        # Defining the model path
        model_path = f"models/{self.crop.strip().lower()}_model.pkl"

        # Splitting the date into day of week, day and month
        df["dayofweek"] = df["Date"].dt.dayofweek
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day

        # Creating lag features
        df["lag_1"] = df["Close"].shift(1)
        df["lag_2"] = df["Close"].shift(2)
        df["lag_3"] = df["Close"].shift(3)

        # Drop rows with NaNs from lagging
        df = df.dropna()

        # Define features and label
        X = df[["dayofweek", "month", "day", "lag_1", "lag_2", "lag_3"]]
        y = df["Close"]

        # Splitting the data into train and test
        X_train = X.iloc[:-1, :]
        y_train = y.iloc[:-1]
        X_test = X.iloc[-1, :]
        X_test = X_test.to_frame().T
        y_test = y.iloc[-1]

        # Defining the list of parameters to be tested
        param_grid = {
            "n_estimators": [50, 100, 200],
            "max_depth": [3, 5, 7, 10],
            "learning_rate": [0.001, 0.01, 0.1],
            "subsample": [0.6, 0.8, 1.0],
            'min_child_weight': [1, 3, 5]
        }

        # Loading the Xgboost Model
        model = XGBRegressor()

        # Performing Grid Search with 3 cross validations
        grid = GridSearchCV(model, param_grid, scoring="neg_mean_squared_error", cv=3)

        # Fitting the training data
        grid.fit(X_train, y_train)

        # Predicting the today's price with the best model
        y_test2 = grid.best_estimator_.predict(X_test)

        # Finding the MSE to check performance
        # print(mean_squared_error([y_test], y_test2))

        # Fitting the entire data
        grid.fit(X, y)

        # Saving the model
        with open(model_path, "wb") as f:
            pickle.dump(grid, f)

        # Displaying success mmessage
        print(f"The {self.crop.strip().lower()} model has been trained and saved successfully!")
        
        # Returning nothing
        return
    

    # Creating a function to predict
    def predict(self):

        # Loading the data
        df = self.load_data()

        # Defining the model path
        model_path = f"models/{self.crop.strip().lower()}_model.pkl"

        # Splitting the date into day of week, day and month
        df["dayofweek"] = df["Date"].dt.dayofweek
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day

        # Creating lag features
        df["lag_1"] = df["Close"].shift(1)
        df["lag_2"] = df["Close"].shift(2)
        df["lag_3"] = df["Close"].shift(3)

        # Drop rows with NaNs from lagging
        df = df.dropna()

        # Retrieving tomorrow's date
        tom_date = date.today() + timedelta(days=1)

        # Splitting tomorrow's date into its respective features to match the training data
        X_pred = pd.DataFrame([{
            "dayofweek": tom_date.weekday(),
            "month": tom_date.month,
            "day": tom_date.day,
            "lag_1": df.iloc[-1]["Close"],
            "lag_2": df.iloc[-2]["Close"],
            "lag_3": df.iloc[-3]["Close"]
        }])

        # Loading the xgboost model
        with open(model_path, "rb") as f:
            grid = pickle.load(f)

        # Predicting the next day price with the best model
        y_pred = grid.best_estimator_.predict(X_pred)[0]

        # Converting the date to string
        tom_date = tom_date.strftime("%Y-%m-%d")

        # Returning the closing price of the next date
        return f"The forecasted price of {self.crop} for tomorrow, {tom_date}: ${y_pred:.2f}"


# Creating the main function
if __name__ == '__main__':


    # Creating objects for each crop
    corn_obj = XgBoost(crop='Corn')
    wheat_obj = XgBoost(crop='Wheat')
    soybeans_obj = XgBoost(crop='Soybeans')

    # Training each crop
    corn_obj.train()
    wheat_obj.train()
    soybeans_obj.train()
    