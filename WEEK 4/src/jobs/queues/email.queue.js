import { Queue } from "bullmq-mock"; // mock queue for in-memory testing

export const emailQueue = new Queue("email-queue", {
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: "exponential", delay: 2000 },
    removeOnComplete: true,
    removeOnFail: false
  }
});

// no Redis connection needed
