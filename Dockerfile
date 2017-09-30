FROM python:slim
MAINTAINER Andrey Vykhodtsev "anvykhod@microsoft.com"

RUN mkdir /app
RUN mkdir -p /root/.bokeh/data
#RUN apt-get update && apt-get install -y git
#COPY C:/10.DEV_REPOS/bokeh/examples /app

#RUN git clone https://github.com/bokeh/bokeh


COPY flask_embed.py /app
COPY requirements.txt /app
ADD templates /app/templates
COPY theme.yaml /app
COPY data/bokeh/sea_surface_temperature.csv.gz /root/.bokeh/data

RUN pip3 install -r app/requirements.txt

#RUN python3 -c "import bokeh;bokeh.sampledata.download()"

WORKDIR /app

RUN chmod 700 ./flask_embed.py

CMD python3 ./flask_embed.py

EXPOSE 8000 5006