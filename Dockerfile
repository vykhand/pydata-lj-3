FROM python:slim
MAINTAINER Andrey Vykhodtsev "anvykhod@microsoft.com"

#RUN mkdir /app
RUN apt-get update && apt-get install -y git
#COPY C:/10.DEV_REPOS/bokeh/examples /app

RUN git clone https://github.com/bokeh/bokeh
COPY requirements.txt /bokeh

RUN pip3 install -r bokeh/requirements.txt

RUN python3 -c "import bokeh;bokeh.sampledata.download()"

WORKDIR /bokeh/examples/howto/server_embed

RUN chmod 700 ./flask_embed.py

CMD python3 flask_embed.py

EXPOSE 8000