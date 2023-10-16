from pydantic import BaseModel
from typing import List

from TTMAPI.models.aception import Aception


class Component(BaseModel):
    # Main Attributes
    id: int = 0
    name: str
    phrases: List[str] = []
    description: str = "No description"

    # TTM attributes
    bestCharPercent: int = 0
    mostCharsMatched: int = 0
    matchedAceptions: List[Aception] = []
    aceptions: List[Aception] = []
    ttm_result: int = 0

    # GPT attributes
    gpt_result: int = 0

    def TextMatch(self, trainText: str):

        for phrase in self.phrases:

            aception = Aception(text=phrase)
            aception.MatchTrainText(
                trainText=trainText)

            self.aceptions.append(aception)
            self.mostCharsMatched =\
                max(self.mostCharsMatched, aception.mostCharsMatched)
            self.bestCharPercent =\
                max(self.bestCharPercent, aception.bestCharPercent)
            if (aception.didItMatch):
                self.matchedAceptions.append(aception)

    def SetPolar(self):
        polar_result = 0
        for aception in self.matchedAceptions:
            if aception.isNegative:
                if polar_result == 1 or polar_result == 2:
                    polar_result = 2
                else:
                    polar_result = -1
            else:
                if polar_result == -1 or polar_result == 2:
                    polar_result = 2
                else:
                    polar_result = 1
        self.ttm_result = polar_result
