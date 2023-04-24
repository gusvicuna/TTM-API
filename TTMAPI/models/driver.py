from pydantic import BaseModel
from typing import List
from TTMAPI.models.component import Component
from TTMAPI.models.aception import Aception


class Driver(BaseModel):
    _id: int
    dbid: str
    name: str
    components: List[Component]

    def TextMatch(self, trainText: Aception, concatenated: bool = True):
        for component in self.components:
            component.TextMatch(
                trainText=trainText,
                concatenated=concatenated)
