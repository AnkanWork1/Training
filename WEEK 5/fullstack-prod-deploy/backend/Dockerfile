FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY src ./src

# install curl
RUN apk add --no-cache curl

CMD ["node", "src/index.js"]
