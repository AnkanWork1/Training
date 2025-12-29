import { loadEnv } from "./config/env.js";
import { config } from "./config/index.js";
import { connectDB } from "./loaders/db.js";
import { loadApp } from "./loaders/app.js";
import { logger } from "./utils/logger.js";

console.log("🔷 Starting server...");
loadEnv(); // Load environment first


async function startServer() {
  const cfg = config(); // read fresh env
  console.log("🔹 DB URI:", cfg.db.uri);

  await connectDB(cfg.db.uri);

  const app = await loadApp();
  const server = app.listen(cfg.port, () => {
    logger.info(`✅ Server started on port ${cfg.port}`);
  });

  // Graceful shutdown
  const shutdown = async (signal) => {
    logger.warn(`⚠️ Received ${signal}. Closing DB & server...`);
    await mongoose.connection.close();
    server.close(() => process.exit(0));
  };

  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
}

startServer();
