from legal_agents_pr.core.exceptions import HandoffError
from legal_agents_pr.schemas.handoff import HandoffRequest


class HandoffManager:
    def __init__(self, max_depth: int = 2, max_total: int = 3) -> None:
        self.max_depth = max_depth
        self.max_total = max_total
        self.completed = 0

    def validate(self, request: HandoffRequest) -> None:
        if request.depth > self.max_depth:
            raise HandoffError("Maximum handoff depth exceeded")
        if self.completed >= self.max_total:
            raise HandoffError("Maximum handoff count exceeded")
        if request.to_agent in request.visited_agents or request.to_agent == request.from_agent:
            raise HandoffError("Handoff cycle detected")
        if not request.reason.strip():
            raise HandoffError("Handoff reason is required")
        self.completed += 1

