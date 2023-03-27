from pydantic import BaseModel
from typing import List

from TTMAPI.models.aception import Aception


class Component(BaseModel):
    name: str
    code_words: List[str]
    phrases: List[str]

    bestWordPercent: int = 0
    bestCharPercent: int = 0

    def GetBestPercents(self, trainText: Aception):
        for code_word in self.code_words:
            for phrase in self.phrases:
                text = f"{code_word.lower()} {phrase.lower()}"
                aception = Aception(text=text)
                aception.MatchTrainText(trainText=trainText)
                if aception.bestCharPercent > self.bestCharPercent:
                    self.bestCharPercent = aception.bestCharPercent
                if aception.bestWordPercent > self.bestWordPercent:
                    self.bestWordPercent = aception.bestWordPercent
