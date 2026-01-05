import dotenv from "dotenv";
import { apiLogger } from "../utils/logger.js";

apiLogger.info({
  service: "api",
  stage: "env"
}, "🔵 env.js running");

export function loadEnv() {
  apiLogger.info({
    service: "api",
    stage: "env"
  }, "🌱 Loading environment variables...");

  const env = process.env.NODE_ENV || "local";

  const envFiles = {
    local: ".env.local",
    dev: ".env.dev",
    prod: ".env.prod",
  };

  const path = envFiles[env] || ".env.local";

  const result = dotenv.config({ path });

  if (result.error) {
    apiLogger.error({
      service: "api",
      stage: "env",
      err: result.error
    }, "❌ Failed to load env file");
    process.exit(1);
  }

  apiLogger.info({
    service: "api",
    stage: "env",
    environment: env
  }, `🌱 Environment loaded: ${env}`);
}
