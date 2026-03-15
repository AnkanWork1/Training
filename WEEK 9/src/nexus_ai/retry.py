import time
from src.nexus_ai.logger import log_event


def retry_agent(agent_name, func, retries=3):

    for attempt in range(retries):

        try:
            return func()

        except Exception as e:

            log_event(agent_name, f"Failure attempt {attempt+1}: {e}")
            time.sleep(1)

    raise Exception(f"{agent_name} failed after {retries} attempts")