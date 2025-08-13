FROM python:3.9

LABEL maintainer "DataMade <info@datamade.us>"

# N.b., this _does not install_ dependencies required to extract text from PDFs.
RUN apt-get update && \
    apt-get install -y gdal-bin && \
    apt-get clean && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --use-feature=fast-deps --use-deprecated=legacy-resolver -r requirements.txt

# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app

# Add a bogus env var for the Django secret key in order to allow us to run
# the 'collectstatic' management command
ENV DJANGO_SECRET_KEY 'foobar'
# Sets Debug to False to make sure that Django compressor can run.
# Unless overridden in docker-compose.yml or .env locally or config variables
# in Heroku, this sets the environment to production mode
ENV DJANGO_DEBUG 'False'

# Build static files into the container
RUN python manage.py collectstatic --noinput
