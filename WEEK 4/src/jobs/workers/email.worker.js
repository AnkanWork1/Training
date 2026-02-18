// src/jobs/workers/email.worker.js
import { emailQueue } from "../queues/email.queue.js"; // memory queue
import { workerLogger } from "../../utils/logger.js";

function processJob(job) {
  const { to, subject, body, requestId } = job.data;
  workerLogger?.info({ jobId: job.id, pid: process.pid, requestId }, "processing email job") ||
    console.log(`[Worker] Processing job ${job.id}`, job.data);

  return new Promise((resolve) => {
    setTimeout(() => {
      workerLogger?.info({ jobId: job.id, pid: process.pid, requestId }, "email job completed") ||
        console.log(`[Worker] Completed job ${job.id}`);
      resolve(true);
    }, 1000); // simulate sending email
  });
}

// register the worker
emailQueue.registerWorker((job) => {
  processJob(job);
});

console.log("Email worker (memory-only) started");
