from pydantic import BaseModel
from TTMAPI.helpers.text import LenOfCharsWithoutSpace, Clean


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

    def MatchTrainText(self,
                       trainText: str,
                       concatenated: bool = True
                       ) -> None:

        cleaned_aception: str = Clean(self.text)
        cleaned_traintext: str = Clean(trainText)
        len_traintext: int = len(list(cleaned_traintext))

        aception_words = dict()

        # Se evalua cada palabra de la acepción
        for word in cleaned_aception.split(" "):
            # print(f"word: {word}")

            aception_words[word] = {
                "didWordMatch": False,
                "finalPosOfMatch": -1,
                "bestCharsMatch": 0
            }

            is_word_matching: bool = False

            # Se recorre la palabra por el textrain
            for word_position in range(len_traintext + len(word)):
                chars_matched: int = 0

                # print("------------")

                # Se recorre cada letra de traintext
                for char_pos_traintext in range(len_traintext):

                    # La position del carácter evaluado en la palabra
                    char_pos_word: int = char_pos_traintext + len(word) -\
                        word_position

                    # Chequear si es el inicio en la palabra y
                    # el traintext, para empezar a revisar match
                    if (char_pos_word == 0):
                        # Si es el inicio del traintext
                        if (char_pos_traintext == 0):
                            is_word_matching = True
                        # O si es el inicio de una palabra entremedio
                        elif (cleaned_traintext[char_pos_traintext - 1]
                                == " "):
                            is_word_matching = True

                    # Se omiten los caracteres fuera de la palabra evaluada
                    if char_pos_word < 0 or char_pos_word >= len(word):
                        continue

                    traintext_char: str = cleaned_traintext[char_pos_traintext]
                    word_char: str = word[char_pos_word]

                    # print(f"    {traintext_char}={word_char}")
                    # Chequeo de si son el mismo caracter
                    are_the_same_char: bool = False
                    if traintext_char == word_char:
                        are_the_same_char = True
                    elif word_char == "@":
                        if traintext_char == "A" or traintext_char == "O":
                            are_the_same_char = True

                    if are_the_same_char:
                        chars_matched += 1
                    else:
                        is_word_matching = False

                    # Chequeo de si cumple condiciones para considerarse
                    # match de palabra
                    did_word_match: bool = False
                    if is_word_matching and char_pos_word == len(word) - 1:
                        if (char_pos_traintext != len_traintext - 1):
                            if (cleaned_traintext[char_pos_traintext + 1]
                                    == " "):
                                did_word_match = True
                        else:
                            did_word_match = True
                    if did_word_match:
                        # print(f"Matched word: {word}")
                        aception_words[word]["didWordMatch"] = True
                        aception_words[word]["finalPosOfMatch"] =\
                            char_pos_traintext

                aception_words[word]["bestCharsMatch"] = max(
                    aception_words[word]["bestCharsMatch"],
                    chars_matched)

            if aception_words[word]["didWordMatch"]:
                self.mostWordsMatched += 1
            self.mostCharsMatched += aception_words[word]["bestCharsMatch"]
