import logging
import json
from datetime import datetime
import os
from deploy.config import LOG_FILE

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id

        if hasattr(record, "endpoint"):
            log_record["endpoint"] = record.endpoint

        return json.dumps(log_record)

def get_logger():
    # Ensure the directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger("llm")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
    return logger