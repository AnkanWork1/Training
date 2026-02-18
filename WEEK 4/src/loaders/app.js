import express from "express";
import productRoutes from "../routes/product.routes.js"; 
import userRoutes from "../routes/userRoutes.js";
import { securityMiddleware } from "../middlewares/security.js";
import { requestLogger } from "../middlewares/logger.js";
import { errorHandler } from "../middlewares/error.middleware.js";
import { requestTracing } from "../utils/tracing.js";
import accountRoutes from "../routes/accounts.routes.js"; 
import emailRoutes from "../routes/email.routes.js";

export async function loadApp() {
  const app = express();
  securityMiddleware(app); 
  app.use(express.json());
  app.use(requestTracing);
  app.use(requestLogger);

  
  
  
  // Ping route
  app.get("/ping", (req, res) => res.send("pong"));

  // Optional root route
  app.get("/health", (req, res) => res.send("Hello Day kebdwebwe"));


  // Accounts routes -> day 2
  app.use("/accounts", accountRoutes);

  // Product routes-> day 3
  app.use("/products", productRoutes);

  // routes -> Day 4

  app.use("/api/users", userRoutes);

  //worker routes -> Day 5
  app.use("/api", emailRoutes);

  app.use(errorHandler);


  return app;
}