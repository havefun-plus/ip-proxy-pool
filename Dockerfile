FROM python:3.6
MAINTAINER fcy "cangyufu@gmail.com"

ENV REFRESHED_AT 2019-03-10-01
ENV REDIS_HOSTNAME=redis
ENV CRONJOB_SETTINGS=ipfeeder.settings
ENV PYTHONPATH=.

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r deploy/requirements/prod.txt
CMD ["gunicorn", "-c", "deploy/gunicorn.conf.py", "ipfeeder.web.views:app"]
