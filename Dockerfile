FROM python:slim-buster
COPY . .
RUN apt-get update && apt-get install git -y
RUN pip3 install -r requirements.txt
CMD python3 bot.py
