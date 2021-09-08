FROM python:slim-buster
RUN apt-get update && apt-get install git -y
RUN pip3 install -U pip && pip3 install -r requirements.txt
COPY . .
CMD python3 -m bot
