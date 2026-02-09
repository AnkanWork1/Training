import dotenv from "dotenv";
import { apiLogger } from "../utils/logger.js";

apiLogger.info({
  service: "api",
  stage: "env"
}, "🔵 env.js running");

export function loadEnv() {
  const env = process.env.NODE_ENV || "local";

  const envFiles = {
    local: ".env.local",
    dev: ".env.dev",
    prod: ".env.prod",
  };

  const path = envFiles[env] || ".env.local";

  const result = dotenv.config({ path });

  if (result.error) {
    // ❌ DO NOT log here
    // ❌ DO NOT call process.exit()
    throw new Error(`Failed to load env file: ${result.error.message}`);
  }

  // Only log after env is loaded
  apiLogger.info({
    service: "api",
    stage: "env",
    environment: env
  }, `🌱 Environment loaded: ${env}`);
}

