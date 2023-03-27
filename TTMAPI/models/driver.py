from pydantic import BaseModel
from typing import List
from TTMAPI.models.component import Component
from TTMAPI.models.aception import Aception


class Driver(BaseModel):
    _id: int
    name: str
    components: List[Component]

    def GetBestPercents(self, trainText: Aception):
        for component in self.components:
            component.GetBestPercents(trainText=trainText)
