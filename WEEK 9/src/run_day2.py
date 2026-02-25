from orchestrator.planner import generate_tasks
from agents.worker_agent import run_task
from agents.reflection_agent import reflect
from agents.validator import validate
from collections import deque
from concurrent.futures import ThreadPoolExecutor

def main():
    user_query = input("User: ").strip()

    # ---------------- Memory for each agent ----------------
    planner_memory = deque(maxlen=10)
    worker_memory = deque(maxlen=10)
    reflection_memory = deque(maxlen=10)
    validator_memory = deque(maxlen=10)

    # ---------------- Planner ----------------
    tasks_text = generate_tasks(user_query, planner_memory)
    tasks = [t.strip() for t in tasks_text.split("\n") if t.strip()]

    print("\n--- Planner Tasks ---")
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t}")

    # ---------------- Workers (parallel) ----------------
    worker_outputs = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_task, task, worker_memory) for task in tasks]
        for f in futures:
            worker_outputs.append(f.result())

    print("\n--- Worker Outputs ---")
    for i, o in enumerate(worker_outputs, 1):
        print(f"{i}. {o}")

    # ---------------- Reflection ----------------
    reflection_output = reflect(worker_outputs, reflection_memory)
    print("\n--- Reflection Agent ---")
    print(reflection_output)

    # ---------------- Validator ----------------
    validation_output = validate(reflection_output, validator_memory)
    print("\n--- Validator Agent ---")
    print(validation_output)

if __name__ == "__main__":
    main()