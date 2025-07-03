FROM node:24

WORKDIR /app

COPY package*.json ./
RUN npm cache clean --force && npm ci

EXPOSE 5173

CMD ["npm", "run", "dev"]
