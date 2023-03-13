from pydantic import BaseModel
from typing import List
from TTMAPI.models.component import Component


class Driver(BaseModel):
    _id: int
    name: str
    components: List[Component]
