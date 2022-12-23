###
### Jupyter for https://github.com/falkolav/cell-counter
###
### base image found here https://hub.docker.com/_/python
## see here for python-cuda images: https://hub.docker.com/r/pure/python
#FROM pure/python:3.6-cuda9.0-cudnn7-runtime AS base
## see here for cuda images https://hub.docker.com/r/nvidia/cuda
#FROM nvidia/cuda:11.4.2-cudnn8-runtime-ubuntu20.04 AS base
FROM python:3.6 AS base

ENV PATH /opt/conda/bin:$PATH
ENV LANG C

### second stage (add Jupyter)
FROM base AS jupyter
#RUN apt-get update && apt install -y pip
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
RUN apt-get --allow-releaseinfo-change update
RUN apt-get install -y libxrender-dev
RUN apt-get install -y libgl1-mesa-glx

### last stage: set user and launch notebook
FROM jupyter AS final
ARG USER_ID
ARG GROUP_ID
EXPOSE 8887

# user and group id are defined in build.sh command

RUN addgroup --gid $GROUP_ID user # name user as user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user # name group user as user
RUN mkdir /my_data
RUN chown user:user /my_data
USER user

CMD jupyter notebook --notebook-dir=/my_data --ip='0.0.0.0' --port='8887' --allow-root --NotebookApp.token='' --NotebookApp.password=''
