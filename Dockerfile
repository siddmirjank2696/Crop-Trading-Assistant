# Choosing a base image
FROM python:3.10-slim

# Setting working directory inside the container
WORKDIR /app

# Copying all contents of the folder inside app
COPY . /app

# Installing thr dependencies
RUN pip install -r requirements.txt

# Exposing a port for the app
EXPOSE 8501

# Executing the streamilt app
CMD ["streamlit", "run", "src/crop_assistant.py", "--server.port=8501", "--server.address=0.0.0.0"]
