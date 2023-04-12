from pydantic import BaseModel
from TTMAPI.helpers.text import LenOfCharsWithoutSpace, CleanText


class Aception(BaseModel):

    text: str
    mostWordsMatched: int = 0
    mostCharsMatched: int = 0
    bestWordPercent: int = 0
    bestCharPercent: int = 0

    def __str__(self) -> str:
        return f"{self.text}"

    def getWordPercent(self):
        self.bestWordPercent = round(
            self.mostWordsMatched * 100 / len(self.text.split(" ")), 2)
        return self.bestWordPercent

    def getCharPercent(self):
        self.bestCharPercent = round(
            self.mostCharsMatched * 100 / LenOfCharsWithoutSpace(self.text), 2)
        return self.bestCharPercent

    def MatchTrainText(self, trainText: str) -> None:
        cleaned_text = CleanText(self.text)
        cleaned_traintext = CleanText(trainText)
        len_traintext = len(list(cleaned_traintext))
        len_aception = len(cleaned_text)

        for aception_pos in range(len_traintext + len_aception):

            chars_matched = 0
            words_matched = 0

            pos_delay = 0
            # print("------------")
            for word in cleaned_text.split(" "):
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
                        continue

                    traintext_char = cleaned_traintext[char_pos_traintext]
                    word_char = word[char_id]
                    # print(f"    {traintext_char}={word_char}")
                    are_the_same_char = traintext_char == word_char

                    if are_the_same_char:
                        chars_matched += 1
                    else:
                        is_word_matching = False

                    if is_word_matching and char_id == len(word) - 1:
                        if (char_pos_traintext != len_traintext - 1):
                            if (cleaned_traintext[char_pos_traintext + 1] == " "):
                                # print(is_word_matching)
                                words_matched += 1
                        else:
                            # print(is_word_matching)
                            words_matched += 1

                pos_delay += len(word) + 1

            self.mostWordsMatched = max(self.mostWordsMatched, words_matched)
            self.mostCharsMatched = max(self.mostCharsMatched, chars_matched)
