# Importing required libraries
import os
import warnings
from langchain.tools import tool
from langchain.chat_models import BedrockChat
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from market_sentiment import MarketSentiment


# Creating a function to analyze market and wrapping it in a langchain tool
@tool
def analyze_market(crop):

    """ This function analyzes the market and provides the market sentiment """

    # Creating an instance of the MarketSentiment class
    crop_obj = MarketSentiment(crop)

    # Retrieving the market sentiment
    market_sentiment = crop_obj.market_sentiment()

    # Returning the market sentiment
    return market_sentiment


# Creating a class MarketAdvisorAgent
class MarketAdvisorAgent:


    # Creating a constructor to initialize attributes
    def __init__(self, crop):

        # Initialzing the crop
        self.crop = crop


    # Creating a function to create the agent
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
            tools=[analyze_market],
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )

        # Returning the agent
        return agent
    

    # Creating a function to execute the agent
    def execute_agent(self):

        # Creating the agent
        agent = self.create_agent()

        # Defining the user prompt
        user_prompt = f"What's the market sentiment for {self.crop}"

        # Executing the agent
        response = agent.run(user_prompt)

        # Returning the response
        return response
    

# Creating the main function
if __name__ == '__main__':


    # Enter the crop for which the market sentiment needs to be observed
    crop = input("Please enter the crop for which you want market advise!\n")

    # Creating an instance of MarketAdvisorAgent class
    agent_obj = MarketAdvisorAgent(crop)

    # Generating a response
    response = agent_obj.execute_agent()

    # Displaying the response
    print(response)