import { Queue } from "bullmq";
import IORedis from "ioredis";

const connection = new IORedis(process.env.REDIS_URL);

export const emailQueue = new Queue("email-queue", {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: "exponential",
      delay: 2000
    },
    removeOnComplete: true,
    removeOnFail: false
  }
});
