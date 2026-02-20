from deployment.query_router import QueryRouter
from deployment.retrieval_dispatcher import RetrievalDispatcher
from deployment.memory import SessionMemory


class Day5Orchestrator:

    def __init__(self):
        self.router = QueryRouter()
        self.dispatcher = RetrievalDispatcher()
        self.memory = SessionMemory()

    def handle(
        self,
        session_id: str,
        mode: str,
        query: str = None,
        image: str = None,
        db: str = None
    ):

        self.memory.add(session_id, "user", query or image)

        route = self.router.route(mode)

        if route == "text":
            result = self.dispatcher.run_text(query)

        elif route == "image":
            result = self.dispatcher.run_image(image)

        elif route == "sql":
            result = self.dispatcher.run_sql(db, query)

        else:
            raise ValueError("Unsupported mode")

        self.memory.add(session_id, "system", result["stdout"])

        return {
            "result": result,
            "memory": self.memory.get(session_id)
        }
