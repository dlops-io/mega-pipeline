FROM node:14.5.0-alpine as build

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
ENV PUBLIC_URL /

COPY package.json ./
COPY yarn.lock ./
RUN yarn install

COPY . ./
RUN yarn run build

# Nginx wrapper to serve static files
FROM nginx:stable
RUN rm -rf /etc/nginx/conf.d
COPY conf /etc/nginx

COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]