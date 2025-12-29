import pino from "pino";
console.log("🟢 logger.js running");
export const logger = pino({
  transport: { target: "pino-pretty", options: { colorize: true } }
});
