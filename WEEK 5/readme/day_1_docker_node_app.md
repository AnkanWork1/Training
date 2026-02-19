# Day 1: Run Node.js App in Docker

## Objective
Run the Node.js application in a Docker container to ensure local containerized development setup.

## Steps Taken



1. **Build Docker image (create image)**

Run this command from the directory where your Dockerfile is present.

docker build -t node-app .

2. **Run the Node.js app in Docker:**
```bash
docker run -d \
  --name my-node-app-dev \
  -p 3000:3000 \
  -v ~/Desktop/Learning/my-node-app:/usr/src/app \
  node-app
```

3. **Verify the container is running:**
```bash
docker ps
```
Expected output:
```
CONTAINER ID   IMAGE      COMMAND             STATUS         PORTS                 NAMES
<id>           node-app   "docker-entrypoint…" Up X seconds 0.0.0.0:3000->3000/tcp my-node-app-dev
```

4. **Verify application response**
curl http://localhost:3000

5. **Go inside the running container (like SSH)**
docker exec -it my-node-app-dev /bin/sh

6. **Run commands inside the container**



- pwd
- ls
- ps aux
- env

7. **Stop the running container**
docker stop my-node-app-dev

8. **Remove the container**
docker rm my-node-app-dev


## Deliverables
- Node.js app is running in Docker container: `my-node-app-dev`
- Port 3000 mapped correctly
- App accessible at `http://localhost:3000`

## Notes
- Ensure old containers or processes on port 3000 are removed to avoid conflicts.
- Volume mounting allows local code changes to reflect inside the container.

