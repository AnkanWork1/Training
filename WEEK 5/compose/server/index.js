import express from "express";
import mongoose from "mongoose";
import os from "os";

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

app.get("/api/health", (req,res) => {
	res.json({
	status: "ok",
	server: os.hostname()
	});
});
app.get("/", (req, res) => {
  res.send("Server is running");
});

app.listen(3000, () => {
  console.log("🚀 Server running on port 3000");
});

