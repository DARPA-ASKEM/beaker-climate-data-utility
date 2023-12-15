FROM ghcr.io/darpa-askem/beaker-kernel:latest

USER root

# RUN apt add-repository ppa:ubuntugis/ppa
RUN apt-get update &&\
    apt-get install -y build-essential gcc g++ gdal-bin libgdal-dev python3-all-dev libspatialindex-dev


ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal


RUN pip install numpy==1.24.3 

WORKDIR /elwood_context
COPY --chown=1000:1000 . /elwood_context/

RUN pip install hatch

USER jupyter
RUN pip install .



WORKDIR /jupyter
CMD ["python", "/jupyter/service/dev.py", "--ip", "0.0.0.0", "-y"]
