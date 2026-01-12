# SSL Setup & HTTPS — Day 4

## Objective

Enable HTTPS for local development using self-signed certificates (mkcert) and configure NGINX as a reverse proxy with load balancing for multiple Node backends.

---

## 1. Generate Self-Signed Certificates (mkcert)

1. Install mkcert (if not already):

```bash
mkcert -install
```

2. Create a folder for certificates:

```bash
mkdir -p certs
```

3. Generate certificates for local domain `myapp.local`:

```bash
mkcert -cert-file certs/myapp.local.pem -key-file certs/myapp.local-key.pem myapp.local
```

> Output:
>
> * `certs/myapp.local.pem` → certificate
> * `certs/myapp.local-key.pem` → private key

---

## 2. Map Local Domain

Add to `/etc/hosts`:

```
127.0.0.1 myapp.local
```

This allows the browser to resolve `myapp.local` locally.

---

## 3. Prepare NGINX Configuration

Create `nginx.conf`:

```nginx
events {}

http {
    upstream backend_service {
        server backend1:3000;
        server backend2:3000;
        # round-robin load balancing
    }

    # HTTP → HTTPS redirect
    server {
        listen 80;
        server_name myapp.local;
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl;
        server_name myapp.local;

        ssl_certificate     /etc/nginx/certs/myapp.local.pem;
        ssl_certificate_key /etc/nginx/certs/myapp.local-key.pem;

        location /api/ {
            proxy_pass http://backend_service;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

---

## 4. Run Node Backends

```bash
docker network create app-net

docker run -d --name backend1 --network app-net -v "$(pwd)/server:/app" -w /app node:20-alpine sh -c "npm install && node index.js"
docker run -d --name backend2 --network app-net -v "$(pwd)/server:/app" -w /app node:20-alpine sh -c "npm install && node index.js"
```

> Verify backends:

```bash
docker ps
```

---

## 5. Run NGINX Reverse Proxy with SSL

```bash
docker run -d \
  --name nginx-proxy \
  --network app-net \
  -p 80:80 \
  -p 443:443 \
  -v "$(pwd)/nginx.conf:/etc/nginx/nginx.conf" \
  -v "$(pwd)/certs:/etc/nginx/certs:ro" \
  nginx
```

---

## 6. Test HTTPS & Load Balancing

```bash
curl -k https://myapp.local/api/health
```

* Should return JSON from backend1 or backend2:

```json
{"status":"ok","server":"backend1"}
{"status":"ok","server":"backend2"}
```

* Multiple requests alternate between backends → confirms **round-robin load balancing**.

---

## 7. Browser Test

* Open `https://myapp.local` in browser
* Should show **lock icon** (HTTPS active)
* API endpoints `/api/health` should respond correctly

---

## ✅ Notes

1. `node:20-alpine` containers are minimal — no curl installed inside; test from host or NGINX.
2. NGINX must have **correct certificate paths** (`nginx.conf` → `/etc/nginx/certs/...`).
3. Port 443 must be exposed in Docker (`-p 443:443`).
4. HTTP → HTTPS redirect ensures all traffic is encrypted locally.
