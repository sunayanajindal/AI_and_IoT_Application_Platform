FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install requests
RUN pip3 install Flask
COPY WrapperClass.py /
COPY model1.pkl /
CMD python3 WrapperClass.py