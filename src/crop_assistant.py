# Importing required libraries
import streamlit as st
from routing_agent import RoutingAgent


# Creating a class CropAssistant
class CropAssistant:


    # Creating a constructor to initialize attributes
    def __init__(self):

        # Initlaizing the attributes
        self.page_title = "Crop Trading Assistant"
        self.title = "Crop Trading Assistant"
        self.placeholder_text = "Hi! Currently, I can forecast predictions or generate market sentiment for Corn, Soybeans or Wheat. What would you like me to do?"
        self.user_prompt = ""

    
    # Creating a function to create the page layout
    def create_layout(self):

        # Setting the page title
        st.set_page_config(page_title=self.page_title, layout="centered")
        st.title(self.title)

        # Adding background color
        st.markdown(
            """
            <style>
            .stApp {
                background-color: cyan;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Getting user input
        self.user_prompt = st.text_input(self.placeholder_text)


    # Creating a function to run the app
    def run(self):

        # Creating the layout
        self.create_layout()

        # Performing an action when submit button is clicked
        if(st.button("Submit")):
    
            # Creating an instance of the RoutingAgent class
            agent_obj = RoutingAgent(self.user_prompt)

            # Trying the operation
            try:

                # Generating the response
                response = agent_obj.execute_agent()

            # Handling exception
            except ValueError as e:

                # Generating response
                response = "I apologize! Too many requests have been made lately. Please wait a little while before trying again."

            # Displaying the response on the UI
            st.success(f"{response}")
        

# Creating the main function
if __name__ == "__main__":


    # Creating the instance of the class CropAssistant
    app = CropAssistant()

    # Exacuting the app
    app.run()

        
