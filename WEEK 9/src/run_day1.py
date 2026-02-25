from collections import deque
from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.answer_agent import answer_agent

# Memory windows
research_memory = deque(maxlen=10)
summarizer_memory = deque(maxlen=10)
answer_memory = deque(maxlen=10)

def main():
    while True:
        user_query = input("User: ").strip()
        if user_query.lower() in {"exit", "quit"}:
            break

        # ---------------- Research agent ----------------
        research_memory.append({"role": "user", "content": user_query})
        research_result = research_agent.generate_reply(messages=list(research_memory))
        research_memory.append({"role": "assistant", "content": research_result})
        print("\n--- Research Agent ---\n", research_result)

        # ---------------- Summarizer agent ----------------
        summarizer_memory.append({"role": "user", "content": research_result})
        summary = summarizer_agent.generate_reply(messages=list(summarizer_memory))
        summarizer_memory.append({"role": "assistant", "content": summary})
        print("\n--- Summarizer Agent ---\n", summary)

        # ---------------- Answer agent ----------------
        answer_memory.append({"role": "user", "content": summary})
        final_answer = answer_agent.generate_reply(messages=list(answer_memory))
        answer_memory.append({"role": "assistant", "content": final_answer})
        print("\n--- Answer Agent ---\n", final_answer)

if __name__ == "__main__":
    main()