import uuid

from src.orchestrator.planner import generate_tasks
from src.agents.research_agent import Researcher
from src.agents.coder import Coder
from src.agents.analyst import Analyst
from src.agents.validator import validate
from src.agents.critic import Critic
from src.agents.optimizer import Optimizer
from src.agents.reporter import Reporter
from src.nexus_ai.logger import log_event
from src.nexus_ai.retry import retry_agent
from src.agents.reflection_agent import reflect
from src.agents.improvement_agent import ImprovementAgent

class NexusOrchestrator:

    def __init__(self,llm_config):

        self.improvement = ImprovementAgent(llm_config)
        self.llm_config = llm_config

        self.researcher = Researcher(llm_config)
        self.analyst = Analyst(llm_config)
        self.coder = Coder(llm_config)
        self.critic = Critic(llm_config)
        self.optimizer = Optimizer(llm_config)
        self.reporter = Reporter(llm_config)

    def run(self, query: str):

        trace_id = str(uuid.uuid4())[:8]

        state = {
            "query": query,
            "plan": None,
            "research": None,
            "analysis": None,
            "code": None,
            "critique": None,
            "optimized_code": None,
            "validation": None,
            "report": None,
            "reflection": None,
            "improvement": None
        }

        try:

            log_event("SYSTEM", f"[{trace_id}] Query received: {query}")

            # ----------------------
            # 1. PLANNING
            # ----------------------

            print("\n[1] Planning...")

            state["plan"] = retry_agent(
                "Planner",
                lambda: generate_tasks(query, memory=[])
            )

            log_event("Planner", state["plan"])

            # ----------------------
            # 2. RESEARCH
            # ----------------------

            print("\n[2] Researching...")

            state["research"] = retry_agent(
                "Researcher",
                lambda: self.researcher.run(query)
            )

            log_event("Researcher", state["research"])

            # ----------------------
            # 3. ANALYSIS
            # ----------------------

            print("\n[3] Analyzing...")

            state["analysis"] = retry_agent(
                "Analyst",
                lambda: self.analyst.run(state["research"])
            )

            log_event("Analyst", state["analysis"])

            # ----------------------
            # 4. CODE GENERATION
            # ----------------------

            print("\n[4] Coding...")

            state["code"] = retry_agent(
                "Coder",
                lambda: self.coder.run(query)
            )

            log_event("Coder", state["code"])

            # ----------------------
            # 5. CRITIQUE
            # ----------------------

            print("\n[5] Critiquing...")

            state["critique"] = retry_agent(
                "Critic",
                lambda: self.critic.run(state["code"])
            )

            log_event("Critic", state["critique"])

            # ----------------------
            # 6. OPTIMIZATION
            # ----------------------

            print("\n[6] Optimizing...")

            state["optimized_code"] = retry_agent(
                "Optimizer",
                lambda: self.optimizer.run(state["code"])
            )

            log_event("Optimizer", state["optimized_code"])

            # ----------------------
            # 7. VALIDATION
            # ----------------------

            print("\n[7] Validating...")

            state["validation"] = retry_agent(
                "Validator",
                lambda: validate(state["optimized_code"], memory=[])
            )

            log_event("Validator", str(state["validation"]))

            # ----------------------
            # 8. REPORTING
            # ----------------------

            print("\n[8] Reporting...")

            state["report"] = retry_agent(
                "Reporter",
                lambda: self.reporter.run(
                    query=query,
                    plan=state["plan"],
                    research=state["research"],
                    analysis=state["analysis"],
                    code=state["code"],
                    improved=state["optimized_code"],
                    validation=state["validation"]
                )
            )

            log_event("Reporter", state["report"])

            print("\n[9] Reflection...")

            state["reflection"] = reflect(
                query=query,
                final_answer=state["report"]
            )

            print("\n[10] Self Improvement...")

            state["improvement"] = self.improvement.run(
                reflection=state["reflection"]
            )

            return state["report"], state

        except Exception as e:

            log_event("SYSTEM ERROR", f"[{trace_id}] {str(e)}")

            return f"System failed: {str(e)}"