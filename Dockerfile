# Choosing a base image
FROM python:3.10-slim

# Setting working directory inside the container
WORKDIR /app

# Copying only requirements.txt file
COPY requirements.txt .

# Installing the dependencies
RUN pip install -r requirements.txt

# Copying all contents of the folder inside app
COPY . .

# Creating Streamlit config to override browser address
RUN mkdir -p ~/.streamlit && echo "[server]\naddress = \"0.0.0.0\"\nport = 8501\nheadless = true\nenableCORS = false\n\n[browser]\nserverAddress = \"localhost\"" > ~/.streamlit/config.toml

# Exposing a port for the app
EXPOSE 8501

# Executing the streamilt app
CMD ["streamlit", "run", "src/crop_assistant.py", "--server.port=8501", "--server.address=0.0.0.0"]
