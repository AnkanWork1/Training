import { withRequest } from "../utils/logger.js";

export const errorHandler = (err, req, res, next) => {
  const log = withRequest(req);

  log.error(
    {
      err, // pino automatically serializes stack + message
      method: req.method,
      url: req.originalUrl,
      body: req.body,
      params: req.params,
      query: req.query,
      service: "api"
    },
    "Unhandled application error"
  );

  res.status(err.status || 500).json({
    error: err.message || "Internal Server Error",
    requestId: req.requestId
  });
};
