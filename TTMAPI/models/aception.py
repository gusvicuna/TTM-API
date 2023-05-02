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
        # print(f"{self.text}: {LenOfCharsWithoutSpace(self.text)}")
        self.bestCharPercent = round(
            self.mostCharsMatched * 100 / LenOfCharsWithoutSpace(self.text), 0)
        return self.bestCharPercent

    def MatchTrainText(self,
                       trainText: str,
                       concatenated: bool = True
                       ) -> None:

        cleaned_aception: str = Clean(self.text)
        cleaned_traintext: str = Clean(trainText)
        len_traintext: int = len(list(cleaned_traintext))

        # Se evalua cada palabra de la acepción
        for word in cleaned_aception.split(" "):

            # Chequear si la palabra viene con paréntesis
            (did_have_parenthesis): bool = False
            did_have_slash: bool = False
            splited_word: str = word.split("(")
            extra: str = ""
            splited_extra: list = []
            if (len(splited_word) > 1):
                (did_have_parenthesis) = True
                word = splited_word[0]
                extra = splited_word[1][:-1]

                # Chequear si el parentesis viene con slash
                splited_extra = extra.split("/")
                if (len(splited_extra) > 1):
                    did_have_slash = True

            did_word_match: bool = False
            bestCharsMatch: bool = False

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
                    are_the_same_char = self.AreTheSameChar(
                        traintext_char, word_char)

                    if are_the_same_char:
                        chars_matched += 1
                    else:
                        is_word_matching = False

                    # Chequeo de si cumple condiciones para considerarse
                    # match de palabra
                    if is_word_matching and char_pos_word == len(word) - 1:

                        if (char_pos_traintext == len_traintext - 1):
                            if (not did_have_slash):
                                did_word_match = True

                        elif (cleaned_traintext[char_pos_traintext + 1]
                                == " "):
                            if (not did_have_slash):
                                did_word_match = True

                        elif (did_have_parenthesis):
                            if (not did_have_slash):
                                word = word + extra
                            else:
                                # Repetir en caso de tener parentesis con slash
                                # TODO: Optimizar esto
                                for single_extra in splited_extra:
                                    is_extra_matching: bool = True
                                    extra_chars_matched: int = 0
                                    for idx, x in enumerate(single_extra):
                                        if (char_pos_traintext + idx + 1 == len_traintext):
                                            break
                                        # Chequeo de si son el mismo caracter
                                        traintext_char = cleaned_traintext[char_pos_traintext + idx + 1]
                                        are_the_same_char = self.AreTheSameChar(traintext_char, x)
                                        if are_the_same_char:
                                            extra_chars_matched += 1
                                        else:
                                            is_extra_matching = False
                                    if is_extra_matching:
                                        if (char_pos_traintext + len(single_extra) >= len_traintext - 1):
                                            if (char_pos_traintext + len(single_extra) == len_traintext - 1):
                                                did_word_match = True
                                        elif (cleaned_traintext[char_pos_traintext + len(single_extra) + 1] == " "):
                                            did_word_match = True

                bestCharsMatch = max(bestCharsMatch, chars_matched)

            if did_word_match:
                # print(f"Matched word: {word}")
                self.mostWordsMatched += 1

            self.mostCharsMatched += bestCharsMatch

    def AreTheSameChar(self, traintext_char, word_char):
        are_the_same_char: bool = False
        if traintext_char == word_char:
            are_the_same_char = True
        elif word_char == "@":
            if traintext_char == "A" or traintext_char == "O":
                are_the_same_char = True
        return are_the_same_char
