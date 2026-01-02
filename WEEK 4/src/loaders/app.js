import express from "express";
import { logger } from "../utils/logger.js";
import productRoutes from "../routes/product.routes.js"; // if you have product routes
import userRoutes from "../routes/userRoutes.js";
import { securityMiddleware } from "../middlewares/security.js";


export async function loadApp() {
  logger.info("🚀 Bootstrapping application");

  const app = express();
  securityMiddleware(app); // attach globally

  app.use(express.json());
  logger.info("🧩 Middlewares loaded");
// Ping route
  app.get("/ping", (req, res) => res.send("pong"));

  // Optional root route
  app.get("/", (req, res) => res.send("Hello Day kebdwebwe"));

  // Product routes
  app.use("/products", productRoutes);
  logger.info("🛣 Routes mounted: 1 endpoint");

  app.use("/api/users", userRoutes);
  logger.info("🛣 Routes mounted: /api/users endpoint");

  return app;
}
