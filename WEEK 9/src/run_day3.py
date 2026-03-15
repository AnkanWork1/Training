from tools.query_generator import generate_task
from orchestrator.orchestrator import route


def main():

    print("\nDAY-3 Tool-Calling Agents (LLM based)")
    print("Type 'exit' to quit\n")

    while True:

        user_query = input("Enter your query: ").strip()

        if user_query.lower() == "exit":
            break

        task = generate_task(user_query)

        print("\nStructured Task:\n", task)

        print("\n[Orchestrator] Routing...\n")

        result = route(task)

        print("Final result:\n", result)
        print("-" * 60)


if __name__ == "__main__":
    main()