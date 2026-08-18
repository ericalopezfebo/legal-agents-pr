import pytest
from pydantic import BaseModel

from legal_agents_pr.core.exceptions import ConfigurationError
from legal_agents_pr.providers.registry import default_registry
from legal_agents_pr.tools import Tool, ToolRegistry


def test_unknown_provider():
    with pytest.raises(ConfigurationError):
        default_registry().create("unknown")


class Input(BaseModel):
    value: str


class Output(BaseModel):
    value: str


class Echo(Tool):
    name = "echo"
    description = "Offline test tool"
    input_schema = Input
    output_schema = Output

    async def execute(self, payload: BaseModel) -> BaseModel:
        return Output(value=payload.value)


def test_tool_registry_rejects_duplicates():
    registry = ToolRegistry()
    registry.register(Echo())
    assert registry.get("echo").name == "echo"
    with pytest.raises(ValueError):
        registry.register(Echo())

