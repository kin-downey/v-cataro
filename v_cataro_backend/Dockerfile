FROM python:3.8

COPY ../../v_cataro_backend/requirements.txt /run

COPY ../../v_cataro_backend/entrypoint-api.sh /run

WORKDIR /run

RUN pip install -r requirements.txt

RUN mkdir /run/v_cataro_backend

EXPOSE 8000

CMD [ "sh", "entrypoint-api.sh" ]