FROM ubuntu:24.04
WORKDIR /app
COPY . /app
COPY supervisord.conf /etc/supervisord.conf
RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev python3-lxml \
    && pip3 install virtualenv \
    && pip3 install supervisor \
    && virtualenv venv \
    && . venv/bin/activate \
    && pip3 install -r requirements.txt \
    && pip3 install gunicorn uvicorn \
    && chmod +x entrypoint.sh \
    && chmod +x flask.sh \
    && chmod +x backend.sh
EXPOSE 5001
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "${PATH}:/app"
ENTRYPOINT ["./entrypoint.sh"]