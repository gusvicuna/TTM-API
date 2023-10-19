from pydantic import BaseModel


class Prompt(BaseModel):
    id: int
    name: str = "no name"
    modifiable_instruction: str = "no instruction"
    unmodifiable_instruction: str = "no instruction"
