// backend/index.js
import express from "express";
import os from "node:os";

const app = express();
const port = 3000;

app.get("/api", (req, res) => {
  res.send(`Hello from ${os.hostname()}\n`);
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Backend listening on ${port}`);
});
