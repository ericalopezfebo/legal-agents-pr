import pytest

from legal_agents_pr.core.exceptions import HandoffError
from legal_agents_pr.core.handoffs import HandoffManager
from legal_agents_pr.schemas.handoff import HandoffRequest


def request(**changes):
    data = {
        "from_agent": "administrative-law", "to_agent": "constitutional-law",
        "issue": "due process", "reason": "specialized constitutional analysis",
        "visited_agents": ["administrative-law"], "depth": 1,
    }
    data.update(changes)
    return HandoffRequest(**data)


def test_valid_handoff():
    HandoffManager().validate(request())


def test_blocks_cycle_and_depth():
    manager = HandoffManager(max_depth=1)
    with pytest.raises(HandoffError):
        manager.validate(request(depth=2))
    with pytest.raises(HandoffError):
        manager.validate(request(visited_agents=["administrative-law", "constitutional-law"]))

