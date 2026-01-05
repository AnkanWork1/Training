# ============================
# ENVIRONMENT VARIABLES
# ============================
.env.example:
  NODE_ENV: local
  PORT: 3000
  DB_URI: mongodb://localhost:27017/day5
  REDIS_URL: redis://127.0.0.1:6379
  LOG_LEVEL: info

# ============================
# LOGGER SETUP
# src/utils/logger.js
# ============================
logger.js: |
  import pino from "pino";
  import path from "path";
  import fs from "fs";

  const logDir = path.join(process.cwd(), "src/logs");
  if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });

  const logFile = path.join(logDir, "app.log");

  const logger = pino(
    {
      level: process.env.LOG_LEVEL || "info",
      timestamp: pino.stdTimeFunctions.isoTime,
    },
    pino.destination(logFile)
  );

  export default logger;

# ============================
# EXPRESS APP
# src/loaders/app.js
# ============================
app.js: |
  import express from "express";
  import emailRoutes from "../routes/email.routes.js";
  import { errorHandler } from "../middlewares/error.middleware.js";
  import { requestTracer } from "../middlewares/tracing.middleware.js";

  export async function loadApp() {
    const app = express();
    app.use(express.json());
    app.use(requestTracer);

    app.use("/api", emailRoutes);
    app.use(errorHandler);

    return app;
  }

# ============================
# SERVER ENTRY POINT
# src/server.js
# ============================
server.js: |
  import { loadApp } from "./loaders/app.js";
  import { connectDB } from "./loaders/db.js";
  import { config } from "./config/index.js";
  import { loadEnv } from "./config/env.js";
  import logger from "./utils/logger.js";

  loadEnv();

  async function startServer() {
    const cfg = config();
    await connectDB(cfg.db.uri);
    const app = await loadApp();
    const PORT = cfg.port || 3000;
    app.listen(PORT, () => logger.info(`✅ Server running on port ${PORT}`));
  }

  startServer();

# ============================
# ROUTES
# src/routes/email.routes.js
# ============================
email.routes.js: |
  import express from "express";
  import { enqueueEmail } from "../jobs/email.job.js";

  const router = express.Router();

  router.post("/notify", async (req, res, next) => {
    try {
      const { to, subject, body } = req.body;
      const requestId = req.requestId || "no-id";
      await enqueueEmail({ to, subject, body, requestId });
      res.status(200).json({ message: "Email job queued", requestId });
    } catch (err) {
      next(err);
    }
  });

  export default router;

# ============================
# JOB QUEUE
# src/jobs/email.job.js
# ============================
email.job.js: |
  import { emailQueue } from "./queues/email.queue.js";
  import logger from "../utils/logger.js";

  export const enqueueEmail = async ({ to, subject, body, requestId }) => {
    try {
      await emailQueue.add("send-email", { to, subject, body, requestId });
      logger.info({ message: "Email job queued", requestId });
    } catch (err) {
      logger.error({ message: "Failed to enqueue email", requestId, err });
    }
  };

# ============================
# WORKER
# src/jobs/workers/email.worker.js
# ============================
email.worker.js: |
  import { Worker } from "bullmq";
  import logger from "../../utils/logger.js";

  const connection = {
    host: "127.0.0.1",
    port: 6379,
    maxRetriesPerRequest: null
  };

  const emailWorker = new Worker("email", async job => {
    const { to, subject, body, requestId } = job.data;
    logger.info({ jobId: job.id, requestId }, "Email job started");

    // simulate email sending
    await new Promise(res => setTimeout(res, 2000));

    logger.info({ jobId: job.id, requestId }, "Email job completed");
  }, { connection });

# ============================
# DEPLOYMENT NOTES
# DEPLOYMENT-NOTES.md
# ============================
DEPLOYMENT-NOTES.md: |
  # Day-5 Deployment Notes — Async Workers & Observability

  ## Prerequisites
  - Node.js >= v20
  - Redis server on 127.0.0.1:6379
  - MongoDB running and URI configured
  - PM2 for production (optional)

  ## Environment Variables


NODE_ENV=local
PORT=3000
DB_URI=mongodb://localhost:27017/day5
REDIS_URL=redis://127.0.0.1:6379
LOG_LEVEL=info


## Install Dependencies
```bash
npm install

Start Services

Redis: redis-server

API: node src/server.js

Worker: node src/jobs/workers/email.worker.js

Testing

POST /api/notify → queues email job

GET /ping → health check

Check app.log for queued jobs

Check worker.log for job processing

Logging & Observability

Structured JSON logs

Each request/job tagged with X-Request-ID

Avoid flooding logs from health checks

Production Deployment (PM2)
pm2 start src/server.js --name api
pm2 start src/jobs/workers/email.worker.js --name worker
pm2 save
pm2 logs

BullMQ Job Handling

Jobs queued in Redis

Retry + exponential backoff configured

Worker logs start & completion per job

Notes

Redis must be running before API & worker

Keep .env.example updated

Filter or throttle /ping logs

============================
POSTMAN COLLECTION (YAML version)
============================

postman.collection.yaml: |
info:
name: "Day-5 Async Email API"
schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json
"
item:
- name: "Send Email"
request:
method: POST
header:
- key: "Content-Type"
value: "application/json"
body:
mode: raw
raw: |
{
"to": "test@example.com
",
"subject": "Hello from Day 5",
"body": "This is a test email from the async job system"
}
url:
raw: "http://localhost:3000/api/notify
"
protocol: http
host: ["localhost"]
port: "3000"
path: ["api","notify"]
- name: "Ping Server"
request:
method: GET
url:
raw: "http://localhost:3000/ping
"
protocol: http
host: ["localhost"]
port: "3000"
path: ["ping"]

