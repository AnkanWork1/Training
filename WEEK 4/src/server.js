import { loadApp } from "./loaders/app.js";
import { connectDB } from "./loaders/db.js";
import { config } from "./config/index.js";
import { loadEnv } from "./config/env.js";
import { apiLogger } from "./utils/logger.js";

loadEnv();

async function startServer() {
  const cfg = config();

  try {
    apiLogger.info(
      {
        service: "api",
        stage: "bootstrap"
      },
      "Starting server bootstrap"
    );

    // Connect MongoDB
    await connectDB(cfg.db.uri);
    apiLogger.info(
      {
        service: "api",
        stage: "database"
      },
      "MongoDB connected"
    );

    // Load Express app
    const app = await loadApp();
    apiLogger.info(
      {
        service: "api",
        stage: "app"
      },
      "Express app loaded"
    );

    // Start server
    const PORT = cfg.port || 3000;
    app.listen(PORT, () => {
      apiLogger.info(
        {
          service: "api",
          stage: "listen",
          port: PORT
        },
        `Server running on port ${PORT}`
      );
    });
  } catch (err) {
    apiLogger.error(
      {
        err,
        service: "api",
        stage: "fatal"
      },
      "Server failed to start"
    );
    process.exit(1);
  }
}

startServer();
