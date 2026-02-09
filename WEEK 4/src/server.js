// src/server.js
import { loadApp } from "./loaders/app.js";
import { connectDB } from "./loaders/db.js";
import { config } from "./config/index.js";
import { loadEnv } from "./config/env.js";
import { apiLogger } from "./utils/logger.js";

// Load environment variables first
loadEnv();

// Start the server
startServer();

async function startServer() {
  try {
    console.log("🔹 Starting server bootstrap");

    const cfg = config();
    console.log("🔹 Config loaded:", {
      env: process.env.NODE_ENV,
      port: cfg.port,
      dbUri: cfg.db?.uri,
    });

    // Connect MongoDB
    console.log("🔹 Connecting to MongoDB...");
    await connectDB(cfg.db.uri);
    console.log("✅ MongoDB connected");

    // Load Express app
    console.log("🔹 Loading Express app...");
    const app = await loadApp();
    console.log("✅ Express app loaded");

    // Start server
    const PORT = cfg.port || 4000;
    app.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
      apiLogger.info(
        {
          service: "api",
          stage: "listen",
          port: PORT,
        },
        `Server successfully started`
      );
    });
  } catch (err) {
    console.error("❌ Server failed to start:", err);
    apiLogger.error(
      {
        err,
        service: "api",
        stage: "fatal",
      },
      "Server failed to start"
    );
    process.exit(1);
  }
}
