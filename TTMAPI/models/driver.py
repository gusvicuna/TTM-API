from pydantic import BaseModel
from typing import List
from TTMAPI.models.component import Component
from TTMAPI.models.aception import Aception


class Driver(BaseModel):
    _id: int
    dbid: str
    name: str
    components: List[Component]
    negatives: Component
    isPositive: bool = True

    def TextMatch(self, trainText: Aception):
        did_have_match: bool = False
        for component in self.components:
            component.TextMatch(trainText=trainText)
            if component.mostWordsMatched >= 1:
                did_have_match = True
        if did_have_match:
            self.negatives.TextMatch(trainText=trainText)
            if self.negatives.mostWordsMatched >= 1:
                self.isPositive = False
