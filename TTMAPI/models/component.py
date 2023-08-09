from pydantic import BaseModel
from typing import List

from TTMAPI.models.aception import Aception


class Component(BaseModel):
    name: str
    phrases: List[str]
    description: str

    bestCharPercent: int = 0
    mostCharsMatched: int = 0
    matchedAceptions: List[Aception] = []
    aceptions: List[Aception] = []

    result: int = 0

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
        for aception in self.matchedAceptions:
            if aception.isNegative:
                if self.result == 1 or self.result == 2:
                    self.result = 2
                else:
                    self.result = -1
            else:
                if self.result == -1 or self.result == 2:
                    self.result = 2
                else:
                    self.result = 1
