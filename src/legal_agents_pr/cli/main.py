from __future__ import annotations

import argparse
import json
import sys

from legal_agents_pr import LegalAgent
from legal_agents_pr.core.config import RuntimeConfig
from legal_agents_pr.core.exceptions import LegalAgentsError
from legal_agents_pr.core.loader import AgentLoader
from legal_agents_pr.core.router import DomainRouter
from legal_agents_pr.providers.registry import default_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="legal-agents-pr")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List installed agents")
    info = sub.add_parser("info", help="Show an agent definition")
    info.add_argument("agent")
    route = sub.add_parser("route", help="Route a legal question")
    route.add_argument("query")
    ask = sub.add_parser("ask", help="Run a specialist agent")
    ask.add_argument("agent", help="Agent id or 'auto'")
    ask.add_argument("query")
    ask.add_argument("--provider")
    ask.add_argument("--model")
    ask.add_argument("--config")
    ask.add_argument("--output", choices=("text", "json"), default="text")
    sub.add_parser("doctor", help="Check local configuration")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    loader = AgentLoader()
    try:
        if args.command == "list":
            for agent_id in loader.list_ids():
                print(agent_id)
            return 0
        if args.command == "info":
            print(loader.load(args.agent).definition.model_dump_json(indent=2))
            return 0
        if args.command == "route":
            print(DomainRouter(loader).route(args.query).model_dump_json(indent=2))
            return 0
        if args.command == "doctor":
            config = RuntimeConfig.load()
            doctor_result = {
                "configuration": "valid",
                "selected_provider": config.provider,
                "selected_model": config.model,
                "known_providers": default_registry().names(),
                "agents": loader.list_ids(),
            }
            print(json.dumps(doctor_result, ensure_ascii=False, indent=2))
            return 0
        agent_id = DomainRouter(loader).route(args.query).primary_agent if args.agent == "auto" else args.agent
        agent = LegalAgent.load(
            agent_id, provider=args.provider, model=args.model, config_path=args.config
        )
        analysis_result = agent.run(args.query)
        print(
            analysis_result.model_dump_json(indent=2)
            if args.output == "json"
            else analysis_result.narrative
        )
        return 0
    except (LegalAgentsError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
