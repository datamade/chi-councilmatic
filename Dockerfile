FROM python:3.7

LABEL maintainer "DataMade <info@datamade.us>"

# N.b., this _does not install_ dependencies required to extract text from PDFs.
RUN apt-get update && \
    apt-get install -y gdal-bin && \
    apt-get clean && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app

ENTRYPOINT ["scripts/docker-entrypoint.sh"]
