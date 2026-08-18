from legal_agents_pr.core.handoffs import HandoffManager
from legal_agents_pr.schemas.handoff import HandoffRequest

handoff = HandoffRequest(
    from_agent="administrative-law",
    to_agent="constitutional-law",
    issue="procedural due process",
    reason="The administrative question contains a distinct constitutional issue.",
    visited_agents=["administrative-law"],
)
HandoffManager(max_depth=2).validate(handoff)
print(handoff.model_dump_json(indent=2))

