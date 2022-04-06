FROM python:3
COPY . /app
WORKDIR /app/Sensor_Registration
RUN pip3 install certifi
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install requests
ENV FLASK_APP=createJSON.py
# CMD [ "python3", "-m" , "sensor_registration.py", "--host=0.0.0.0"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]