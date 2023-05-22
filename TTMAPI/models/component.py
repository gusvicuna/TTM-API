from pydantic import BaseModel
from typing import List

from TTMAPI.models.aception import Aception


class Component(BaseModel):
    name: str
    phrases: List[str]

    bestCharPercent: int = 0
    mostWordsMatched: int = 0
    mostCharsMatched: int = 0
    aceptions: List[Aception] = []

    def TextMatch(self, trainText: Aception):

        for phrase in self.phrases:

            aception = Aception(text=phrase)
            aception.MatchTrainText(
                trainText=trainText.text)

            self.aceptions.append(aception)
            self.mostCharsMatched =\
                max(self.mostCharsMatched, aception.mostCharsMatched)
            self.bestCharPercent =\
                max(self.bestCharPercent, aception.getCharPercent())
            if (aception.didItMatch):
                self.mostWordsMatched += 1
