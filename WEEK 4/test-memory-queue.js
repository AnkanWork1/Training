import { emailQueue } from "./src/jobs/queues/email.queue.js";

(async () => {
  console.log("Adding test jobs to in-memory queue...");

  for (let i = 1; i <= 5; i++) {
    const job = await emailQueue.add({
      to: `test${i}@example.com`,
      subject: `Hello ${i}`,
      body: `This is email ${i}`,
      requestId: `req-${i}`
    });

    console.log(`Added job ${job.id}`);
  }
})();
