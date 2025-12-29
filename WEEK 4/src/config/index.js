// config/index.js
console.log("🔶 config.js running");
export const config = () => ({
  env: process.env.NODE_ENV || "local",
  port: process.env.PORT || 3000,
  db: {
    uri: process.env.DB_URI
  }
});
