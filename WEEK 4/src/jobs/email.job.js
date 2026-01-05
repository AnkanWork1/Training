import { emailQueue } from "./queues/email.queue.js";
import { workerLogger } from "../utils/logger.js";

export const enqueueEmail = async ({ to, subject, body, requestId }) => {
  try {
    await emailQueue.add("send-email", {
      to,
      subject,
      body,
      requestId
    });

    workerLogger.info({
      message: "Email job queued",
      requestId
    });
  } catch (err) {
    workerLogger.error({
      message: "Failed to queue email",
      requestId,
      err
    });
  }
};
