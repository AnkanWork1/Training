/**
 * PM2 Ecosystem Configuration
 * Production ready
 */

module.exports = {
  apps: [
    {
      name: "api-service",
      script: "src/server.js",

      exec_mode: "cluster",
      instances: "max",

      autorestart: true,
      watch: false,
      max_memory_restart: "512M",

      error_file: "logs/pm2-error.log",
      out_file: "logs/pm2-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss",

      env: {
        NODE_ENV: "production"
      }
    },

    {
      name: "email-worker",
      script: "src/jobs/workers/email.worker.js",
      exec_mode: "fork",
      autorestart: true,

      env: {
        NODE_ENV: "production"
      }
    }
  ]
};
