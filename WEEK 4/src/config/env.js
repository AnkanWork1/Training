import dotenv from "dotenv";
console.log("🔵 env.js running");
export function loadEnv() {
    console.log("🌱 Loading environment variables...");
  const env = process.env.NODE_ENV || "local";

  const envFiles = {
    local: ".env.local",
    dev: ".env.dev",
    prod: ".env.prod",
  };

  const path = envFiles[env] || ".env.local";

  const result = dotenv.config({ path });

  if (result.error) {
    console.error("❌ Failed to load env file", result.error);
    process.exit(1);
  }

  console.log(`🌱 Environment loaded: ${env}`);
}
