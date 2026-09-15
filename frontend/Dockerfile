# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
ENV CYPRESS_INSTALL_BINARY=0
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# Optional: copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.config
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]