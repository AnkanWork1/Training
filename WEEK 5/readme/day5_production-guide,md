# Day 5 – Production Guide  
## Full-Stack Deployment with Docker, NGINX & HTTPS

---

## 1. Purpose of Day-5

The goal of Day-5 was **not to add new features**, but to make the system:

- Secure
- Stable
- Production-ready
- Deployable using real-world practices

By the end of Day-5, the application is no longer “just running” —  
it is **ready to survive in production**.

---

## 2. Final Architecture

```
Browser
↓ HTTPS (443)
NGINX (Reverse Proxy & TLS)
├── / → Frontend (static files)
└── /api → Backend (Node.js API)
```


Key points:
- NGINX is the **only public entry point**
- Backend is **never exposed directly**
- HTTPS is handled only by NGINX
- Everything runs inside Docker

---

## 3. Environment Configuration

### `.env` (DO NOT COMMIT)
```env
APP_PORT=3000
NODE_ENV=production
```

### `.env.example` (COMMIT)
```env
APP_PORT=
NODE_ENV=
```
Why this matters

- Code stays the same across environments

- Configuration changes without code changes

- Secrets are never committed

---

## 4. Backend Container Design
What was done

- Backend runs in a Docker container

- Uses environment variables

- Exposes API endpoints:

    - /api

    - /api/health

- Security rule followed

- Backend uses expose, not ports

- Backend is accessible only inside Docker network

- This prevents direct public access.

---

## 5. Health Checks (Critical for Production)
Why health checks matter

- A container being “running” does not mean the app is healthy.

- Implementation

    - /api/health endpoint added

- Docker healthcheck configured

### Result

- Docker knows when the app is healthy

- Enables monitoring and auto-recovery

---

## 6. Restart Policy (Self-Healing)
```restart: unless-stopped```

Why this matters

- Apps can crash unexpectedly

- Docker automatically restarts containers

- Reduces downtime without human intervention

---

## 7. Logging Strategy (What Was Actually Used)
- Logging approach used in Day-5

- Docker-level logging only

- Logs captured from ``stdout / stderr``

- Log rotation enabled

```
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```
#### Important clarification

- No application-level file logging was implemented

- logs/ folder was not actively used

- Focus was on infrastructure log safety, not log formatting

- This prevents disk exhaustion in production.

---

## 8. Docker Compose Profiles
Why profiles were used

- Separate development and production behavior

- Prevent accidental misconfiguration

- Usage
    ```
    docker compose --profile dev up -d
    docker compose --profile prod up -d
    ```

#### Key lesson

- If profiles are defined, Docker will not start services unless a profile is selected.

---

## 9. Reverse Proxy with NGINX
Why NGINX was added

- Single entry point

- Request routing

- HTTPS handling

- Frontend serving

   #### Routing rules
    ``/api`` → Backend container

    ``/`` → Frontend static files

- Users never talk directly to the backend.

---

## 10. HTTPS Implementation
What was done

- Local TLS certificates created using mkcert

- HTTPS enabled in NGINX

- HTTP redirected to HTTPS

- Important design rule

- HTTPS terminates at NGINX

- Backend remains HTTP internally

- This is standard production architecture.

---

## 11. Frontend Deployment
- Frontend strategy

    - Served as static files

    - No frontend server running

    - Mounted directly into NGINX

    - Benefits

    - Faster

    - More secure

    - No CORS issues

    - Single domain setup

    - Frontend uses relative API paths (/api).

--- 

## 12. Docker Networking

- All services run on a private Docker bridge network

- Service-to-service communication via service names

- No hardcoded IP addresses

- This ensures portability and reliability.

---

## 13. Deployment Workflow
1. Configure environment variables
2. Start backend container
3. Start NGINX reverse proxy
4. Enable HTTPS
5. Serve frontend via NGINX
6. Verify health endpoint
7. Monitor logs via Docker

---

## 14. Common Mistakes Avoided

- Exposing backend ports

- Serving HTTP in production

- Hardcoding secrets

- Infinite log growth

- Multiple public entry points

- Editing containers manually


## To stop

`docker compose --profile dev down`

`docker compose --profile prod down`

## To check the status

- `https://localhost/api`

- `https://localhost/api/health`