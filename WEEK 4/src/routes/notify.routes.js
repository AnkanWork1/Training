import express from "express";
import { enqueueEmail } from "../jobs/email.job.js";

const router = express.Router();

router.post("/notify", async (req, res, next) => {
  const { to, subject, body } = req.body;

  await enqueueEmail({
    to,
    subject,
    body,
    requestId: req.requestId
  });

  res.status(202).json({
    message: "Notification queued",
    requestId: req.requestId
  });
});

export default router;
