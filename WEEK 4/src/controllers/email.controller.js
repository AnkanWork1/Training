import { enqueueEmailJob } from "../jobs/email.job.js";

export const sendEmail = async (req, res, next) => {
  try {
    const { to, subject, body } = req.body;

    const job = await enqueueEmailJob({
      to,
      subject,
      body,
      requestId: req.requestId
    });

    res.status(202).json({
      message: "email job queued",
      jobId: job.id,
      requestId: req.requestId
    });
  } catch (e) {
    next(e);
  }
};
