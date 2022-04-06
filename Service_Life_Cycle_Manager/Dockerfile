FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install requests
RUN pip3 install paramiko
RUN pip install azure-storage-file-share

CMD python3 initializer.py