FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install numpy==1.21.5
RUN pip3 install Flask
RUN pip3 install requests
RUN pip3 install kafka-python
RUN pip3 install pymongo
RUN pip3 install sklearn
CMD ["python3","-m","flask","run","--host=0.0.0.0"]