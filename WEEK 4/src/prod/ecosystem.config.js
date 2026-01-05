export default {
  apps: [
    {
      name: "api",
      script: "src/server.js",
      instances: 1,
      exec_mode: "fork"
    },
    {
      name: "email-worker",
      script: "src/jobs/workers/email.worker.js"
    }
  ]
};
