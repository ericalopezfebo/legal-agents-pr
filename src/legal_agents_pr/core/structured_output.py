from pydantic import BaseModel


def parse_structured_output(content: str, schema: type[BaseModel]) -> BaseModel:
    return schema.model_validate_json(content)

