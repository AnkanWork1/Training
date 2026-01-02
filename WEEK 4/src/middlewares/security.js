import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import express from "express";

export const securityMiddleware = (app) => {
  // Secure headers
  app.use(helmet());

  // CORS
  app.use(cors({
    origin: ["http://localhost:5173", "https://your-domain.com"],
    methods: ["GET","POST","PUT","DELETE"],
  }));

  // Rate limiting
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 10000,
    message: "Too many requests. Try again later.",
  });
  app.use(limiter);

  // Payload limit
  app.use(express.json({ limit: "10kb" }));
};
