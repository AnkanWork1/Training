import express from "express";
import { logger } from "../utils/logger.js";

export async function loadApp() {
  logger.info("🚀 Bootstrapping application");

  const app = express();

  app.use(express.json());
  logger.info("🧩 Middlewares loaded");

  app.get("/", (req, res) => res.send("Hello Day 1"));
  logger.info("🛣 Routes mounted: 1 endpoint");

  return app;
}
