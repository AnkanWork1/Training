import express from "express";
import { enqueueEmail } from "../jobs/email.job.js";

const router = express.Router();

router.post("/notify", async (req, res, next) => {
  try {
    const { to, subject, body } = req.body;
    const requestId = req.requestId || "no-id"; // tracing middleware injects this

    await enqueueEmail({ to, subject, body, requestId });

    res.status(200).json({
      message: "Email job queued",
      requestId
    });
  } catch (err) {
    next(err);
  }
});

export default router;
