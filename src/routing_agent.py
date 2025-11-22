# Importing required libraries
import os
import warnings
from langchain.chat_models import BedrockChat
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from forecasting_agent import ForecastingAgent
from market_advisor_agent import MarketAdvisorAgent


# Creating a function to execute ForecastingAgent and wrapping it in a langchain tool
@tool
def forecasting_agent(crop):

    """This function will execute the forecasting agent"""

    # Creating an instance of class ForecastingAgent
    agent_obj = ForecastingAgent(crop)

    # Executing the forecasting agent
    response = agent_obj.execute_agent()

    # Returning the response
    return response


# Creating a function to execute MarketAdvisorAgent and wrapping it in a langchain tool
@tool
def market_advisor_agent(crop):

    """This function will execute the market advisor agent"""

    # Creating an instance of the class MarketAdvisorAgent
    agent_obj = MarketAdvisorAgent(crop)

    # Executing the forecasting agent
    response = agent_obj.execute_agent()

    # Returning the response
    return response


# Creating a class RoutingAgent
class RoutingAgent:


    # Creating a constructor to initialize attributes
    def __init__(self, user_prompt):

        # Initializing the user prompt
        self.user_prompt = user_prompt

    
    # Creating the agent
    def create_agent(self):

        # Ignoring the warnings
        warnings.filterwarnings("ignore")

        # Loading environment variables from .env
        load_dotenv()

        # Accessing the Claude 3 Sonnet model
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        # Accessing the llm
        llm = BedrockChat(
            model_id=model_id,
            region_name=aws_region,
            model_kwargs={'temperature' : 0.0}
        )

        # Creating the agent
        agent = initialize_agent(
            llm=llm,
            tools=[forecasting_agent, market_advisor_agent],
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )

        # Returning the agent
        return agent
    

    # Creating a function to execute the agent
    def execute_agent(self):

        # Creating the agent
        agent = self.create_agent()

        # Executing the agent
        response = agent.run(self.user_prompt)

        # Returning the response
        return response
    

# Creating the main function
if __name__ == '__main__':


    # Retrieving the user input
    user_input = input("Hi! Currently, I can forecast predictions or generate market sentiment for Corn, Soybeans or Wheat. What would you like me to do?\n")

    # Creating an instance of the RoutingAgent
    agent_obj = RoutingAgent(user_input)

    # Generating the response
    response = agent_obj.execute_agent()

    # Displaying the response
    print(response)