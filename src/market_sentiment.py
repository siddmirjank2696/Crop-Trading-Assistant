# Importing required libraries
import yfinance as yf
import warnings


# Creating a class MarketSentiment
class MarketSentiment:


    # Creating a constructor to initialize attributes
    def __init__(self, crop):

        # Initializing the crop
        self.crop = crop

    
    # Creating a function to load the data
    def load_data(self):

        # Ignoring the warnings
        warnings.filterwarnings("ignore")

        # Defining the crop symbols
        crop_symbols = {
            "corn" : "ZC=F",
            "wheat" : "ZW=F",
            "soybeans" : "ZS=F"
        }

        # Loading the data for the past 60 days
        df = yf.download(tickers=crop_symbols[self.crop.strip().lower()], period='1y', progress=False)

        # Adding the index as a separate column
        df["Date"] = df.index

        # Resetting the index
        df = df.reset_index(drop=True)

        # Creating a new dataframe with the date and closing price
        new_df = df.loc[:,["Date", "Close"]]

        # Flattening the cloumns to make it a single-index column
        new_df.columns = ['Date' if col[0] == 'Date' else col[0] for col in new_df.columns]

        # Changing the closing price data type to float
        new_df["Close"] = new_df["Close"].astype(float)

        # Returning the new dataframe
        return new_df
    

    # Creating a function to generate market analysis
    def market_analysis(self):

        # Loading the data
        df = self.load_data()

        # Calculating moving averages
        df["MA5"] = df["Close"].rolling(window=5).mean()
        df["MA20"] = df["Close"].rolling(window=20).mean()

        # Calculating daily % change
        df["pct_change"] = round((df["Close"].pct_change() * 100), 3)

        # Retrieving the recent percentage change
        recent_change = df["pct_change"].iloc[-1]

        # Creating an empty string to store spike/drop message
        spike_flag = ""

        # Checking for a spike
        if(recent_change > 3):
            spike_flag = "Sudden Spike Detected!"
        elif(recent_change < -3):
            spike_flag = "Sudden Drop Detected!"
        else:
            spike_flag = "No Spike Or Drop Noticed"

        # Retrieving the latest moving averages
        ma5 = df["MA5"].iloc[-1]
        ma20 = df["MA20"].iloc[-1]

        # Creating an empty string to store momentum
        momentum = ""

        # Calculating momentum
        if(ma5 > ma20):
            momentum = "bullish"
        else:
            momentum = "bearish"

        # Creating an empty string to store the recommendation
        recommendation = ""

        # Defining the recommendation
        if(momentum == "bullish" and recent_change > 0):
            recommendation = "Recommendation: Consider Buying!"
        elif(momentum == "bearish" and recent_change < 0):
            recommendation = "Recommendation: Consider Selling!"
        else:
            recommendation = "Recommendation: Wait and Watch!"

        # Returning the required insights
        return momentum, recent_change, spike_flag, recommendation
    

    # Creating a function to generate risk analysis
    def risk_analysis(self):

        # Loading the data
        df = self.load_data()

        # Retrieving the returns
        df["Returns"] = df["Close"].pct_change().dropna()

        # Calculating the volatility
        volatility = df["Returns"].std()

        # Calculating the sharpe ratio
        if(volatility != 0):
            sharpe_ratio = df["Returns"].mean()/volatility
        else:
            sharpe_ratio = 0

        # Calculating the drawdown
        cumulative = (1 + df["Returns"]).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        max_drawdown = drawdown.min()

        # Checking for risks
        if max_drawdown < -0.2:
            risk_flag = "High Drawdown Risk Detected!"
        elif volatility > 0.05:
            risk_flag = "Elevated Volatility!"
        else:
            risk_flag = "Risk Levels Acceptable!"

        # Defining the recommendation
        if sharpe_ratio > 1 and max_drawdown > -0.15:
            recommendation = "Risk-adjusted returns look favorable!"
        elif sharpe_ratio < 0.5 or max_drawdown < -0.25:
            recommendation = "Exercise caution, risk is high!"
        else:
            recommendation = "Neutral stance advised!"

        # Returning the required insights
        return volatility, sharpe_ratio, max_drawdown, risk_flag, recommendation
    

    # Creating a function to generate the market sentiment
    def market_sentiment(self):

        # Generating market analysis
        momentum, recent_change, spike_flag, sentiment_recommendation = self.market_analysis()

        # Generating risk analysis
        volatility, sharpe_ratio, max_drawdown, risk_flag, risk_recommendation = self.risk_analysis()

        # Returning the analysis
        return (
            f"Market Sentiment for {self.crop}:\n"
            f"- Momentum: {momentum}\n"
            f"- Latest % change: {recent_change:.2f}%\n"
            f"{spike_flag}\n"
            f"{sentiment_recommendation}\n\n"
            f"Risk & Drawdown Analysis for {self.crop}:\n"
            f"- Volatility: {volatility:.4f}\n"
            f"- Sharpe Ratio: {sharpe_ratio:.2f}\n"
            f"- Max Drawdown: {max_drawdown:.2%}\n"
            f"{risk_flag}\n"
            f"Recommendation: {risk_recommendation}"
        )
    

# Creating the main function
if __name__ == '__main__':


    # Enter the crop for which the market sentiment needs to be observed
    crop = input("Please enter the crop for which you want to see the market sentiment!\n")

    # Creating an instance of the class MarketSentiment
    crop_obj = MarketSentiment(crop)

    # Retrieving the market sentiment
    market_sentiment = crop_obj.market_sentiment()

    # Displaying the market sentiment
    print(market_sentiment)