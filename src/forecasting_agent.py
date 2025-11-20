# Importing required libraries
import os
import warnings
from xgboost_forecasting import XgBoost
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import BedrockChat


# Creating a function to perform forecasting and wrapping it in a tool
@tool
def forecast(crop):

    """Predicts tomorrow's price for a given crop (corn, wheat, soybeans)."""

    # Creating an instance of the XgBoost class
    crop_obj = XgBoost(crop)

    # Forecasting the price
    forecast = crop_obj.predict()

    # Returning the forecast
    return forecast


# Creating a class ForecastingAgent
class ForecastingAgent:


    # Creating a constructor to initialize the attributes
    def __init__(self, crop):

        # Initializing the crop
        self.crop = crop

    
    # Creating a function to define the agent
    def create_agent(self):

        # Ignoring the warnings
        warnings.filterwarnings("ignore")

        # Loading environment variables from .env
        load_dotenv()

        # Accessing the Claude 3 Sonnet model
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        # Defining the llm
        llm = BedrockChat(
            model_id = model_id,
            region_name = aws_region,
            model_kwargs = {'temperature' : 0.0}
        )

        # Initialzing the agent
        agent = initialize_agent(
            llm = llm,
            tools = [forecast],
            agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose = False
        )

        # Returning the agent
        return agent

    
    # Creating a function to execute the agent
    def execute_agent(self):

        # Defining the user prompt
        user_prompt = f"What is the forecast of the price for {self.crop}?"

        # Creating the agent
        agent = self.create_agent()

        # Executing the agent
        response = agent.run(user_prompt)

        # Returning the response
        return response
    

# Creating the main function
if __name__ == '__main__':


    # Enter the crop for which the prediction needs to be made
    crop = input("Please enter the crop for which you want to see the forecast!\n")

    # Creating an instance of the forecasting agent
    agent_obj = ForecastingAgent(crop)

    # Generating the response
    response = agent_obj.execute_agent()

    # Displaying the response
    print(response)