FROM node:18-alpine
WORKDIR /app/frontend
COPY package.json ./
RUN npm install --silent
COPY . .
RUN npm run build
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
