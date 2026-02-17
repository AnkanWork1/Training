import { Worker } from "bullmq";
import IORedis from "ioredis";

const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null
});

const worker = new Worker(
  "email-queue",
  async (job) => {
    const { to, subject, body } = job.data;

    console.log("Email job started", job.id, to);

    // simulate sending email
    await new Promise((r) => setTimeout(r, 500));

    console.log("Email job completed", job.id);
  },
  {
    connection
  }
);

worker.on("failed", (job, err) => {
  console.error("Email job failed", job?.id, err);
});
