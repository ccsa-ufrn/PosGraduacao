FROM python:3.5
ADD . /minerva
WORKDIR /minerva
EXPOSE 3001
RUN pip install -r requirements.txt
