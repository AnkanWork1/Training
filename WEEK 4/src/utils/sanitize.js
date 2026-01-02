import xss from "xss";

export const sanitizeObject = (obj) => {
  const sanitized = {};

  for (const key in obj) {
    if (typeof obj[key] === "string") {
      sanitized[key] = xss(obj[key]);
    } else {
      sanitized[key] = obj[key];
    }
  }

  return sanitized;
};
