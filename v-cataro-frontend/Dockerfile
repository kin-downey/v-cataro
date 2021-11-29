FROM node:12.20.0-alpine3.10

COPY ../../v-cataro-frontend/entrypoint.sh /run

RUN mkdir /run/frontend

EXPOSE 8080

RUN npm install -g @vue/cli

WORKDIR /var/run/frontend

CMD [ "/bin/sh", "/run/entrypoint.sh" ]