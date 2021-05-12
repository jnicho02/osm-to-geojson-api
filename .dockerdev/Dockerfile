FROM debian:latest

RUN apt-get -qq update && apt-get -qq -y install curl bzip2 \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3.6 \
    && conda update conda \
    && apt-get -qq -y remove bzip2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes

ARG NODE_MAJOR

RUN mkdir -p /app
WORKDIR /app

COPY requirements_conda.txt requirements.txt
RUN conda config --add channels conda-forge
RUN conda install -c anaconda scipy
# RUN pip install overpass
RUN pip install qwikidata
RUN conda install --file requirements.txt

# Add NodeJS to sources list
RUN apt-get -qq -y install curl
RUN curl https://deb.nodesource.com/setup_$NODE_MAJOR.x | bash -
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends nodejs

# Add Serverless Framework
RUN npm install -g serverless serverless-python-requirements
