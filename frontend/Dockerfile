# Dockerfile
FROM nginx:latest

# Copy the frontend files into the Nginx html directory
COPY . /usr/share/nginx/html

# Copy the Nginx configuration file (if you have one)
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80
