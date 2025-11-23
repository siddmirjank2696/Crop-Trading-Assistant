# Crop-Trading-Assistant

This product is an AI Assistant that helps farmers trade crop commodites (Corn, Wheat & Soybeans) based on the forecasts and market analysis. It helps farmers make smarter decisions about their harvest by turning complex market data into simple advice. Every day, it forecasts crop prices and analyzes market sentiment to recommend whether they should buy, sell, or wait, so they can maximize profits and reduce risk. With a simple app they can use on any device, farmers get clear, updated guidance without needing to study charts or news, giving them confidence and peace of mind in a fast‑changing market.

### Prerequisites

1. Have an AWS Account

2. Have an IAM User

3. Have access keys generated for that IAM user

### Steps to follow to use this product

1. Install git. You can download it from [this website](https://git-scm.com/install/)

2. Download docker. You can download it from [this website](https://www.docker.com/)

3. Start Docker Desktop to keep the docker engine running

4. Open Git Bash

5. Clone this repository locally <br>
```bash
 git clone https://github.com/siddmirjank2696/Crop-Trading-Assistant.git 
```

6. Navigate into the repository <br>
```bash 
cd .\Crop-Trading-Assistant 
```

7. Create a file named .env <br>
```bash
touch .env
```

8. Add your AWS credentials in the .env file (Replace with your AWS credentials)
```bash
echo "AWS_ACCESS_KEY_ID = <Enter your AWS access key here>" >> .env
echo "AWS_SECRET_ACCESS_KEY = <Enter your AWS secret key here>" >> .env
echo "AWS_REGION = <Enter your AWS region here>" >> .env
```

9. Execute the pipeline<br>
```bash
chmod +x execute_pipeline.sh
./execute_pipeline.sh 
 ```

10. Open your browser and go to localhost:8501 to access the product