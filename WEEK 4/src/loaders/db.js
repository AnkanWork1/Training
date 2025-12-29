import mongoose from "mongoose";
import { logger } from "../utils/logger.js";

export async function connectDB(uri) {
  if (!uri) {
    logger.error("❌ DB_URI is undefined! Check your .env file.");
    process.exit(1);
  }

  try {
    await mongoose.connect(uri); // ✅ no extra options needed
    logger.info("✅ Database connected");
  } catch (err) {
    logger.error("❌ Database connection failed:");
    console.error(err); // full error
    process.exit(1);
  }
}
