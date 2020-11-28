FROM conda/miniconda3:latest

RUN mkdir -p /app
WORKDIR /app

COPY requirements_conda.txt requirements.txt
RUN conda update conda
RUN conda config --add channels conda-forge
RUN conda install -c anaconda scipy
# RUN pip install overpass
RUN conda install --file requirements.txt

# CMD [ "python", "./local.py" ]
