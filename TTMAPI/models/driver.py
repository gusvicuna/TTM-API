from pydantic import BaseModel
from typing import List
from TTMAPI.models.component import Component


class Driver(BaseModel):
    id: int
    name: str = "no name"
    components: List[Component] = []
    positives: Component = []
    negatives: Component = []
    objects: Component = []
    driver_type: str = "driver"

    def AnalyzeText(self,
                    trainText: str,
                    beforeNegDis: int,
                    afterNegDis: int,
                    complete: bool):
        has_a_match = False
        for component in self.components:
            component.TextMatch(trainText=trainText)
            if len(component.matchedAceptions) > 0:
                has_a_match = True
                if complete:
                    self.positives.TextMatch(trainText=trainText)
                    self.objects.TextMatch(trainText=trainText)
                    self.CheckNegatives(
                        trainText,
                        beforeNegDis,
                        afterNegDis,
                        component)
        if self.driver_type == "ut" and not has_a_match:
            self.components[0].ttm_result = 1

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
