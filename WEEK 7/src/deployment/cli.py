import argparse
from deployment.orchestrator import Day5Orchestrator


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--session-id", default="local")
    parser.add_argument("--mode", required=True, choices=["text", "image", "sql"])
    parser.add_argument("--query")
    parser.add_argument("--image")
    parser.add_argument("--db")

    args = parser.parse_args()

    orch = Day5Orchestrator()

    out = orch.handle(
        session_id=args.session_id,
        mode=args.mode,
        query=args.query,
        image=args.image,
        db=args.db
    )

    print(out["result"]["stdout"])


if __name__ == "__main__":
    main()
