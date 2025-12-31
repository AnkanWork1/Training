import express from "express";
import { logger } from "../utils/logger.js";

export async function loadApp() {
  logger.info("🚀 Bootstrapping application");

  const app = express();

  app.use(express.json());
  logger.info("🧩 Middlewares loaded");
// Ping route
  app.get("/ping", (req, res) => res.send("pong"));

  // Optional root route
  app.get("/", (req, res) => res.send("Hello Day kebdwebwe"));

  // Product routes
  app.use("/products", productRoutes);
  logger.info("🛣 Routes mounted: 1 endpoint");

  return app;
}
