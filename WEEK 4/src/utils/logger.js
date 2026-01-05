import pino from "pino";
import path from "path";
import fs from "fs";

// Ensure logs folder exists
const logDir = path.join(process.cwd(), "src/logs");
if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });

/**
 * Base pino config (shared)
 */
const baseConfig = {
  level: process.env.LOG_LEVEL || "info",
  timestamp: pino.stdTimeFunctions.isoTime
};

/**
 * API Logger
 */
const apiLogger = pino(
  baseConfig,
  pino.destination(path.join(logDir, "app.log"))
);

/**
 * Worker Logger
 */
const workerLogger = pino(
  baseConfig,
  pino.destination(path.join(logDir, "worker.log"))
);

/**
 * Create request-scoped logger
 * Adds requestId automatically
 */
export const withRequest = (req) => {
  return apiLogger.child({
    requestId: req.requestId,
    service: "api"
  });
};

export { apiLogger, workerLogger };
