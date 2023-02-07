# ビルド環境
FROM node:latest as build-stage

RUN apt-get update -y && apt-get upgrade -y \
&& rm -rf /var/lib/apt/lists/* && apt-get clean && apt-get autoclean && apt-get autoremove

WORKDIR /app
COPY . .
RUN npm install && npm run build

# 本番環境
FROM nginx:alpine-slim as production-stage

RUN apk update \
&& mkdir /usr/share/nginx/html/otenkisan
COPY --from=build-stage /app/dist /usr/share/nginx/html/otenkisan

RUN rm -rf /usr/share/nginx/html/otenkisan/json \
&& rm -rf /usr/share/nginx/html/otenkisan/images

WORKDIR /usr/share/nginx/html/otenkisan/
RUN ln -s /var/otenkisan/public/json json \
&& ln -s /var/otenkisan/public/images images
WORKDIR /var/otenkisan
