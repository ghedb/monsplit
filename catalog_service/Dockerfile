FROM python:3

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY ./src/ /srv
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
WORKDIR /srv
EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh"]
