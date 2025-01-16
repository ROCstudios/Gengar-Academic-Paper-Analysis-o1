# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

### Installing React with Nginx in server

Configure Nginx for Frontend and Backend

Install Nginx:

```
sudo yum install nginx -y
```

Set Up Nginx Configuration:

Open the Nginx configuration file:
```
sudo nano /etc/nginx/nginx.conf
```
Add the following server blocks:
```
server {
    listen 8001;
    server_name your-domain.com;

    location / {
        root /var/www/frontend/build;
        index index.html;
        try_files $uri /index.html;
    }
}

server {
    listen 8000;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Replace /var/www/frontend/build with the path to your React build directory.

Restart Nginx:

```
sudo systemctl restart nginx
```

Test Nginx Locally:

Ensure both endpoints work:
```
curl http://127.0.0.1:8001
curl http://127.0.0.1:8000
```
