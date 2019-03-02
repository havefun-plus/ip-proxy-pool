FROM python:3.6
MAINTAINER fcy "cangyufu@gmail.com"

ENV REFRESHED_AT 2019-03-03-01

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-c", "gunicorn.conf.py", "ipfeeder.web.views:app"]

