import { withRequest } from "../utils/logger.js";

export const requestLogger = (req, res, next) => {
  const log = withRequest(req);

  log.info({
    method: req.method,
    url: req.originalUrl
  }, "Incoming request");

  next();
};
