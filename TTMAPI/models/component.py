from pydantic import BaseModel
from typing import List

from TTMAPI.models.aception import Aception


class Component(BaseModel):
    name: str
    phrases: List[str]

    bestCharPercent: int = 0
    mostCharsMatched: int = 0
    matchedAceptions: List[Aception] = []
    aceptions: List[Aception] = []

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
