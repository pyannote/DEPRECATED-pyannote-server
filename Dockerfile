FROM stackbrew/ubuntu:12.04
MAINTAINER Hervé Bredin <bredin@limsi.fr>

# install PyAnnote REST API
RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y gfortran libblas-dev liblapack-dev

ADD . /src
RUN pip install /src

CMD ["python", "-m", "pyannote.server.run"]
EXPOSE 5000
