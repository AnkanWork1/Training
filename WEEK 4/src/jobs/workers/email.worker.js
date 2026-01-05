import { Worker } from "bullmq";
import { workerLogger } from "../../utils/logger.js";
import { emailQueue } from "../queues/email.queue.js";

export const emailWorker = new Worker("email", async job => {
  const { to, subject, body, requestId } = job.data;
  
  workerLogger.info({ jobId: job.id, requestId }, "Email job started");

  // Simulate sending email
  await new Promise(res => setTimeout(res, 2000));

  workerLogger.info({ jobId: job.id, requestId }, "Email job completed");

}, {
  connection: {
    host: "127.0.0.1",
    port: 6379,
    // maxRetriesPerRequest must be null or omitted
    maxRetriesPerRequest: null
  }
});
