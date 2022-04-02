FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install PyJWT
RUN pip3 install requests
RUN pip3 install cgi-tools
RUN pip3 install paramiko
RUN pip3 install pickle-mixin


CMD [ "python3", "-m" , "dashboard.py", "--host=0.0.0.0"]