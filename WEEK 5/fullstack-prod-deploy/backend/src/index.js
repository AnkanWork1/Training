require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");

const app = express();

/* ---------- Config ---------- */
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI;

/* ---------- Middleware ---------- */
app.use(express.json());

/* ---------- Routes ---------- */
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

app.get("/api/hello", (req, res) => {
  res.json({ message: "Backend is working" });
});

/* ---------- Mongo Connection ---------- */
async function connectDB() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log("✅ MongoDB connected");
  } catch (err) {
    console.error("❌ MongoDB connection failed", err);
    process.exit(1);
  }
}

/* ---------- Startup ---------- */
async function startServer() {
  await connectDB();
  app.listen(PORT, () => {
    console.log(`🚀 Backend running on port ${PORT}`);
  });
}

startServer();
