module.exports = {
  apps: [
    {
      name: "api-service",
      script: "../server.js",

      exec_mode: "cluster",
      instances: 1,

      autorestart: true,
      watch: false,
      max_memory_restart: "512M",

      error_file: "../logs/pm2-error.log",
      out_file: "../logs/pm2-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss",

      env: {
        NODE_ENV: "production",
        PORT: 3000,
        REDIS_URL: "redis://localhost:6379",
        LOG_LEVEL: "info"
      }
    },

    {
      name: "email-worker",
      script: "../jobs/workers/email.worker.js",
      exec_mode: "fork",
      autorestart: true,

      error_file: "../logs/email-worker-error.log",
      out_file: "../logs/email-worker-out.log",

      env: {
        NODE_ENV: "production",
        REDIS_URL: "redis://localhost:6379",
        LOG_LEVEL: "info"
      }
    }
  ]
};
