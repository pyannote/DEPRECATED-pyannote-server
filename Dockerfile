# CAMOMILE Processing Framework
#
# VERSION 0.1

FROM stackbrew/ubuntu:12.04
MAINTAINER Hervé Bredin <bredin@limsi.fr>

# install PyAnnote REST API
RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y gfortran libblas-dev liblapack-dev
RUN pip install pyannote.server

# expose python app port
EXPOSE 5000

CMD ["python", "-m", "pyannote.server.run"]
