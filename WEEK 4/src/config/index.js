export const config = () => ({
  port: process.env.PORT,
  db: {
    uri: process.env.DB_URI
  }
});
