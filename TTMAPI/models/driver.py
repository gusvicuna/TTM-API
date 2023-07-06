from pydantic import BaseModel
from typing import List
from TTMAPI.models.component import Component


class Driver(BaseModel):
    _id: int
    dbid: str
    name: str
    components: List[Component]
    positives: Component
    negatives: Component
    objects: Component

    def AnalyzeText(self,
                    trainText: str,
                    beforeNegDis: int,
                    afterNegDis: int):

        for component in self.components:
            component.TextMatch(trainText=trainText)
            if len(component.matchedAceptions) > 0:
                self.positives.TextMatch(trainText=trainText)
                self.objects.TextMatch(trainText=trainText)
                self.CheckNegatives(
                    trainText,
                    beforeNegDis,
                    afterNegDis,
                    component)

    def CheckNegatives(
            self,
            trainText: str,
            beforeNegDis: int,
            afterNegDis: int,
            component: Component):

        component.SetPolar()
        for aception in component.matchedAceptions:
            ini_neg_pos: int =\
                        max(0, aception.startingPosMatch - beforeNegDis)
            end_neg_pos: int =\
                min(len(trainText), aception.endingPosMatch + afterNegDis)
            self.negatives.TextMatch(
                trainText=trainText[ini_neg_pos:end_neg_pos])
            for negative in self.negatives.aceptions:
                if negative.didItMatch:
                    aception.isNegative = not aception.isNegative
