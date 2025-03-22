FROM node:21-alpine

WORKDIR /app

COPY package* .

RUN npm ci

COPY index.js .

CMD node index.js