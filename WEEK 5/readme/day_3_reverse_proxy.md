# Reverse Proxy Architecture — Day 3



## Architecture Flow

Client
  ↓
NGINX (Reverse Proxy)
  ↓
Backend Service (multiple replicas)

---

## Components

### NGINX
- Runs inside a Docker container
- Exposes port 8443
- Routes `/api` requests to backend services
- Performs round-robin load balancing

### Backend Service
- Node.js application
- Multiple running instances
- Not exposed directly to the host
- Accessible only through NGINX

### Command to run the compose file `docker compose up -d --scale backend=2`

### To check whether backend is using round-robin for load balancing or not 
- use this command many 

times:ankanguha@HESTABIT-416:~/Desktop/Training/WEEK 5/fullstack-prod-deploy$ 

`curl -k https://localhost:8443/api
Hello from b93f4551504d`



## Load Balancing
- NGINX uses round-robin load balancing by default
- Requests are distributed evenly across backend replicas
- Docker DNS resolves the backend service name to multiple container IPs

---

## Networking
- All containers run on the same Docker bridge network
- Services communicate using service names
- No hardcoded IP addresses are used

---

## Key Principles Demonstrated
- Reverse proxy pattern
- Internal service routing
- Horizontal scaling
- Load balancing simulation
- Single entry point architecture

---

## Summary
This architecture mirrors real production systems where:
- NGINX handles traffic management
- Backends scale horizontally
- Internal services remain private
- Load balancing improves availability