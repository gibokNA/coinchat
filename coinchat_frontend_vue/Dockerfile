FROM nginx:latest

COPY ./dist /usr/share/nginx/html
COPY ./src/assets /usr/share/nginx/html

COPY ./default.conf /etc/nginx/conf.d/default.conf