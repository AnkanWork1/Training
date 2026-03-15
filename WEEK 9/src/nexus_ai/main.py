import uuid

from src.orchestrator.nexus_orchestrator import NexusOrchestrator
from src.memory.session_memory import SessionMemory
from src.memory.vector_store import VectorStore
from src.llm_config import llm_config

# -------------------------------------------------------
# simple fact extractor
# -------------------------------------------------------
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

    # remove duplicates
    return list(dict.fromkeys(facts))


# -------------------------------------------------------
# build query with recalled memory
# -------------------------------------------------------
def build_query_with_memory(query, recalled):

    if not recalled:
        return query

    memory_block = "RELEVANT MEMORY:\n"

    for r in recalled:
        memory_block += f"- ({r['type']}) {r['content']}\n"

    return f"""
{memory_block}

USER QUERY:
{query}
"""


# -------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------
def main():

    print("\nNEXUS AI (Memory Enabled)")
    print("Type 'exit' to stop\n")

    # memory
    session = SessionMemory()
    store = VectorStore()

    # orchestrator
    nexus = NexusOrchestrator(llm_config)

    while True:

        query = input("User> ").strip()

        if query.lower() == "exit":
            break

        request_id = str(uuid.uuid4())[:8]

        print(f"\n[System] Processing request {request_id}")

        try:

            # --------------------------------------------------
            # 1. MEMORY RECALL
            # --------------------------------------------------
            recalled = store.search(query, k=5)

            query_with_memory = build_query_with_memory(
                query,
                recalled
            )

            # --------------------------------------------------
            # 2. RUN NEXUS PIPELINE
            # --------------------------------------------------
            result = nexus.run(query_with_memory)

            print("\nFINAL OUTPUT:\n")
            print(result)

            # --------------------------------------------------
            # 3. UPDATE SESSION MEMORY
            # --------------------------------------------------
            session.add_message("user", query)
            session.add_message("assistant", result)

            # --------------------------------------------------
            # 4. STORE EPISODIC MEMORY
            # --------------------------------------------------
            episode = f"""
User: {query}

Assistant:
{result}
"""

            store.add_memory(
                text=episode,
                memory_type="episodic",
                metadata={"agent": "nexus"}
            )

            # --------------------------------------------------
            # 5. STORE SEMANTIC MEMORY
            # --------------------------------------------------
            facts = extract_important_facts(session.last_n(6))

            for f in facts:

                store.add_memory(
                    text=f,
                    memory_type="semantic",
                    summary=f,
                    metadata={"agent": "nexus"}
                )

        except Exception as e:

            print("\nSYSTEM ERROR:", e)


# -------------------------------------------------------
if __name__ == "__main__":
    main()