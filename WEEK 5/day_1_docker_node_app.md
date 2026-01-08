# Day 1: Run Node.js App in Docker

## Objective
Run the Node.js application in a Docker container to ensure local containerized development setup.

## Steps Taken

1. **Check port 3000 for existing processes:**
```bash
sudo ss -tulnp | grep :3000
```
2. **Kill any process using port 3000 (if necessary):**
```bash
sudo kill -9 <PID>
```
3. **Remove old Docker containers (if they exist):**
```bash
docker rm my-node-app my-node-app-dev
```
4. **Run the Node.js app in Docker:**
```bash
docker run -d \
  --name my-node-app-dev \
  -p 3000:3000 \
  -v ~/Desktop/Learning/my-node-app:/usr/src/app \
  node-app
```

5. **Verify the container is running:**
```bash
docker ps
```
Expected output:
```
CONTAINER ID   IMAGE      COMMAND             STATUS         PORTS                 NAMES
<id>           node-app   "docker-entrypoint…" Up X seconds 0.0.0.0:3000->3000/tcp my-node-app-dev
```

6. **Verify port mapping:**
```bash
sudo ss -tulnp | grep :3000
```
Expected output shows `docker-proxy` listening on port 3000.

7. **Verify app response (optional):**
```bash
curl http://localhost:3000
```

## Deliverables
- Node.js app is running in Docker container: `my-node-app-dev`
- Port 3000 mapped correctly
- App accessible at `http://localhost:3000`

## Notes
- Ensure old containers or processes on port 3000 are removed to avoid conflicts.
- Volume mounting allows local code changes to reflect inside the container.

