# -- < BUILDER > ---------------------
FROM python:3.8.15 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

# lint
# RUN pip install flake8==3.9.2
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY . .
# RUN flake8 --ignore=E501,F401 .

# -- < Final > -----------------------

FROM python:3.8.15 

RUN apt-get update
RUN apt-get install -y netcat

# -- This should be installed with poetry, fix later TODO
RUN pip install gunicorn
# ------------------------------------

# create the app user
RUN addgroup --system vsf && adduser --system vsf --ingroup vsf

# # create directory for the app user
# RUN mkdir -p /home/vsf

# create the appropriate directories
ENV HOME=/home/vsf
ENV APP_HOME=/home/vsf/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# Install more dependencies 
COPY ./requirements.txt . 
RUN pip install -r requirements.txt --no-cache-dir

# RUN apt-get update && apt-get install libpq

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

COPY . $APP_HOME


# Install project
WORKDIR $APP_HOME/measurement_navigator/vsf
RUN mv /home/vsf/web/run_web_service.sh .
RUN poetry config virtualenvs.create false --local
RUN poetry install && rm -rf ~/.cache/pypoetry/{cache,artifacts}

# chown all the files to the app user
RUN chown -R vsf:vsf $APP_HOME
# change to the app user
USER vsf

# Add local executables 
ENV PATH=${PATH}:$HOME/.local/bin


# run entrypoint.sh
ENTRYPOINT ["/home/vsf/web/entrypoint.sh"]