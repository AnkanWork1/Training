import express from "express";
import mongoose from "mongoose";

const app = express();

const mongoUri = process.env.MONGO_URI;

mongoose
  .connect(mongoUri)
  .then(() => {
    console.log("✅ Mongo connected");
  })
  .catch((err) => {
    console.error("❌ Mongo error:", err);
  });

app.get("/", (req, res) => {
  res.send("Server is running");
});

app.listen(3000, () => {
  console.log("🚀 Server running on port 3000");
});

