import { Queue } from "bullmq";

const connection = {
  url: process.env.REDIS_URL
};

export const EMAIL_QUEUE_NAME =
  process.env.EMAIL_QUEUE_NAME || "email-queue";

export const emailQueue = new Queue(EMAIL_QUEUE_NAME, {
  connection
});

export async function enqueueEmailJob(payload, opts = {}) {
  return emailQueue.add(
    "send-email",
    payload,
    {
      attempts: 3,
      backoff: {
        type: "exponential",
        delay: 2000
      },
      removeOnComplete: true,
      removeOnFail: false,
      ...opts
    }
  );
}
