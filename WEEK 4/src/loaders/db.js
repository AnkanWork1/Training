import mongoose from "mongoose";
import { apiLogger } from "../utils/logger.js";

apiLogger.info(
  {
    service: "api",
    stage: "database"
  },
  "🟢 db.js running"
);

export async function connectDB(uri) {
  if (!uri) {
    apiLogger.error(
      {
        service: "api",
        stage: "database"
      },
      "❌ DB_URI is undefined! Check your .env file."
    );
    process.exit(1);
  }

  try {
    await mongoose.connect(uri);
    apiLogger.info(
      {
        service: "api",
        stage: "database"
      },
      "✅ Database connected"
    );
  } catch (err) {
    apiLogger.error(
      {
        err,
        service: "api",
        stage: "database"
      },
      "❌ Database connection failed"
    );
    process.exit(1);
  }
}
