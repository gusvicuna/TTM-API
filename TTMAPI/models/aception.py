from pydantic import BaseModel
from TTMAPI.helpers.text import LenOfCharsWithoutSpace


class Aception(BaseModel):

    text: str
    mostWordsMatched: int = 0
    mostCharsMatched: int = 0

    def __str__(self) -> str:
        return f"{self.text}"

    def getWordPercent(self):
        return round(
            self.mostWordsMatched * 100 / len(self.text.split(" ")), 2)

    def getCharPercent(self):
        return round(
            self.mostCharsMatched * 100 / LenOfCharsWithoutSpace(self.text), 2)

    def MatchTrainText(self, trainText: str) -> None:
        len_traintext = len(list(trainText))
        len_aception = len(self.text)

        for aception_pos in range(len_traintext + len_aception):

            chars_matched = 0
            words_matched = 0

            pos_delay = 0
            # print("------------")
            for word in self.text.split(" "):
                # print(f"word: {word}")

                is_word_matching = False

                for char_pos_traintext in range(len_traintext):

                    char_id = (len_aception + char_pos_traintext) -\
                        (pos_delay + aception_pos)

                    if char_id == 0:
                        is_word_matching = True
                    if char_id < 0 or char_id > len(word):
                        continue
                    elif char_id == len(word):
                        if is_word_matching:
                            # print(is_word_matching)
                            words_matched += 1
                        continue

                    traintext_char = trainText.upper()[char_pos_traintext]
                    word_char = word.upper()[char_id]
                    # print(f"    {traintext_char}={word_char}")
                    are_the_same_char = traintext_char == word_char

                    if are_the_same_char:
                        chars_matched += 1
                    else:
                        is_word_matching = False

                pos_delay += len(word) + 1

            self.mostWordsMatched = max(self.mostWordsMatched, words_matched)
            self.mostCharsMatched = max(self.mostCharsMatched, chars_matched)
