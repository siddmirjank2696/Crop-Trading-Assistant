# Crop-Trading-Assistant

This product is an AI Assistant that helps farmers trade crop commodites (Corn, Wheat & Soybeans) based on the forecasts and market analysis. It helps farmers make smarter decisions about their harvest by turning complex market data into simple advice. Every day, it forecasts crop prices and analyzes market sentiment to recommend whether they should buy, sell, or wait, so they can maximize profits and reduce risk. With a simple app they can use on any device, farmers get clear, updated guidance without needing to study charts or news, giving them confidence and peace of mind in a fast‑changing market.

### Steps to follow to use this product

1. Install git. You can download it from [this website](https://git-scm.com/install/)

2. Download docker. You can download it from [this website](https://www.docker.com/)

3. Start Docker Desktop to keep the docker engine running

4. Open your terminal

5. Clone this repository locally <br>
` git clone https://github.com/siddmirjank2696/Crop-Trading-Assistant.git `

6. Navigate into the repository <br>
` cd .\Crop-Trading-Assistant `

7. Create a file named .env and add this information inside it <br>
` AWS_ACCESS_KEY_ID = <Enter your AWS access key here>
AWS_SECRET_ACCESS_KEY = <Enter your AWS secret key here>
AWS_REGION = <Enter your AWS region here> `

8. Execute the pipeline in your Terminal<br>
` execute_pipeline.bat `

9. Open your browser and go to localhost:8501 to access the product