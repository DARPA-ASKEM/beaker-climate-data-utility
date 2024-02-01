FROM python:3.10

USER root

# RUN apt add-repository ppa:ubuntugis/ppa
RUN apt-get update &&\
    apt-get install -y build-essential gcc g++ git gdal-bin gfortran libgdal-dev python3-all-dev libspatialindex-dev make npm &&\
    npm install -g typescript

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /climate_data_utility_context

COPY --chown=1000:1000 . /climate_data_utility_context/

# Separate numpy install is a prerequisite for GDAL
RUN pip install numpy==1.24.3 && \ 
    pip install hatch


RUN useradd -m jupyter
USER jupyter
RUN pip install -e .

WORKDIR /jupyter
COPY --chown=1000:1000 default.ipynb /jupyter/
CMD ["python", "-m", "beaker_kernel.server.main", "--ip", "0.0.0.0"]
