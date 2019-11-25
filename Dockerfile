FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3 && \
    apt-get install -y python3-dev && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-pyaudio
RUN apt-get install -y sox && \
    apt-get install -y swig && \
    apt-get install -y libatlas-base-dev
RUN apt-get install -y git
RUN git clone https://github.com/mdeblaauw/lightSwitcher.git
RUN cd lightSwitcher && \
    pip3 install -r requirements.txt && \
    pip3 install -y awscli && \
    cd ../
RUN git clone https://github.com/Kitt-AI/snowboy.git && \
    cd snowboy/swig/Python3/ && \
    make && \
    cd ../../..
RUN cp -rf snowboy/swig/Python3/* lightSwitcher/functions/snowboy/
RUN rm -rf snowboy
WORKDIR /lightSwitcher/

ENTRYPOINT ["python3", "demo.py"]
