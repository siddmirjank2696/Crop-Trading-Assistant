REM Pulling the latest models from GitHub
git pull

REM Building the docker image
docker build -t "crop_assistant_img" .

REM Running the docker image
docker run -p 8501:8501 crop_assistant_img