from src.memory.session_memory import SessionMemory
from src.memory.vector_store import VectorStore
from src.llm_client import LLMClient


llm_config = {
    "config_list": [
        {
            "model": "local-llama",
            "base_url": "http://127.0.0.1:8000/v1",
            "api_key": "none",
            "max_tokens": 200
        }
    ],
    "cache_seed": None
}


# ------------------------------------------------------------
# simple fact extractor
# (replace with LLM based summarizer later)
# ------------------------------------------------------------
def extract_important_facts(messages):

    facts = []

    for m in messages:
        text = m["content"].lower()

        if "i am" in text or "i'm" in text:
            facts.append(m["content"])

        if "project" in text:
            facts.append(m["content"])

        if "working on" in text:
            facts.append(m["content"])

    return list(dict.fromkeys(facts))


# ------------------------------------------------------------
def build_prompt(session, recalled, user_input):

    memory_block = ""

    if recalled:
        memory_block += "RELEVANT MEMORY:\n"
        for r in recalled:
            memory_block += f"- ({r['type']}) {r['content']}\n"

    history_block = ""
    for m in session.get_messages():
        history_block += f"{m['role']}: {m['content']}\n"

    prompt = f"""
You are an assistant.

{memory_block}

CONVERSATION:
{history_block}

USER: {user_input}
ASSISTANT:
"""
    return prompt


# ------------------------------------------------------------
def main():

    session = SessionMemory()
    store = VectorStore()
    llm = LLMClient(llm_config)

    print("\nMemory Agent Demo (local llama)")
    print("Type 'exit' to stop.\n")

    while True:

        user_input = input("You> ").strip()

        if user_input.lower() == "exit":
            break

        # 1. recall
        recalled = store.search(user_input, k=5)

        # 2. build prompt
        prompt = build_prompt(session, recalled, user_input)

        # 3. generate
        try:
            answer = llm.generate(prompt)
        except Exception as e:
            print("LLM error:", e)
            continue

        print("\nAssistant>\n", answer, "\n")

        # 4. short-term memory
        session.add_message("user", user_input)
        session.add_message("assistant", answer)

        # 5. episodic memory
        episode = f"User: {user_input}\nAssistant: {answer}"

        store.add_memory(
            text=episode,
            memory_type="episodic",
            metadata={"agent": "default"}
        )

        # 6. semantic memory
        facts = extract_important_facts(session.last_n(6))

        for f in facts:
            store.add_memory(
                text=f,
                memory_type="semantic",
                summary=f,
                metadata={"agent": "default"}
            )


if __name__ == "__main__":
    main()