FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/drman.conf /etc/nginx/conf.d/
