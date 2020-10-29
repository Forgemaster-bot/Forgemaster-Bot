FROM python:3

## Install FreeTDS and dependencies for PyODBC
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc  && apt-get install --reinstall build-essential -y && apt-get clean -y

## Install MSODBC Driver from Microsoft's package website
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install msodbcsql17 mssql-tools unixodbc-dev -y

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

## Set working directory - this is where python requires our applications
WORKDIR /usr/src/app

## Copy requirements.txt and install needed packages
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

## Copy our application over
COPY . ./
RUN rm -r venv
## Overwrite credentials with test credentials
COPY tests/Credentials ./Credentials

## Set the PYTHONPATH ENV for our application
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/Modules"
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/cogs"

## DEBUG: ls current directory to verify install
RUN ls -la .

## Add wait scripts to allow waiting for sql server to be up and running
COPY tests/automation/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

## Remove unneeded files
RUN find -name '*.pyc' -delete
RUN find -name __pycache__ -delete

## Run the bot application
#CMD ["pytest"]
