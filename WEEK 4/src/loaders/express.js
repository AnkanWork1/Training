import express from "express";
import routes from "../routes/index.js";
import { logger } from "../utils/logger.js";

export function loadExpress() {
  const app = express();

  app.use(express.json());

  let routeCount = 0;
  routes(app, () => routeCount++);

  logger.info(`🛣 Routes mounted: ${routeCount} endpoints`);

  return app;
}
