FROM python:3.10
LABEL maintainer "DataMade <info@datamade.us>"

# N.b., this _does not install_ dependencies required to extract text from PDFs.
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  gdal-bin \
  ca-certificates \
  curl && \
  apt-get clean && \
  rm -rf /var/cache/apt/* /var/lib/apt/lists/*

# Heroku's container runtime doesn't honor layer deletions, so CA symlinks that
# ca-certificates removes from /etc/ssl/certs reappear on the dyno. The bundle
# file is regenerated (not deleted), so it comes through clean: point OpenSSL
# clients (curl, git, Python's stdlib ssl) at the bundle and an empty CApath.
RUN mkdir -p /etc/ssl/empty-capath
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
  SSL_CERT_DIR=/etc/ssl/empty-capath

WORKDIR /app

# Install pip from source and upgrade setuptools and certifi
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
  python get-pip.py --no-cache-dir && \
  rm get-pip.py && \
  pip install --no-cache-dir setuptools "certifi>=2026.10.19"

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
