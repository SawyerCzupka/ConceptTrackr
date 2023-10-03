ARG NODE_VERSION=18.18.0

FROM node:${NODE_VERSION}-slim

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .