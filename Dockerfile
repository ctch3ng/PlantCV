FROM ubuntu

RUN apt-get update && apt-get install -y git wget gedit sudo

WORKDIR /workspace

RUN git clone https://github.com/danforthcenter/plantcv.git

WORKDIR /workspace/plantcv

RUN mv ./scripts/common.sh ./scripts/common.bak

RUN sed 's/apt-get install/apt-get install -y/' ./scripts/common.bak > ./scripts/common.sh

RUN mv ./scripts/setup.sh ./scripts/setup.bak

RUN sed 's/pip install/yes \| pip install/' ./scripts/setup.bak > ./scripts/setup.sh

RUN bash ./scripts/setup.sh

RUN apt-get update && apt-get install -y python-tk

WORKDIR /workspace

ENV PATH="/workspace/plantcv/venv/bin:${PATH}"
ENV PYTHONPATH="/usr/lib/python2.7/dist-packages:${PYTHONPATH}"