from pydantic import BaseModel
from TTMAPI.helpers.text import Clean


class Aception(BaseModel):

    text: str
    mostCharsMatched: int = 0
    bestCharPercent: int = 0
    didItMatch: bool = False
    isNegative: bool = False

    def __str__(self) -> str:
        return f"{self.text}"

    def getCharPercent(self):
        cleaned_text = self.text.split("(")
        self.bestCharPercent =\
            round(self.mostCharsMatched * 100 / (len(cleaned_text[0]) + 2), 0)
        self.bestCharPercent = min(self.bestCharPercent, 100)
        return self.bestCharPercent

    def MatchTrainText(self,
                       trainText: str,
                       ) -> None:

        cleaned_aception: str = Clean(self.text)
        cleaned_traintext: str = Clean(trainText)

        # Chequear negativo
        if (cleaned_aception[0] == "-"):
            print(cleaned_aception[1:])
            self.isNegative = True
            cleaned_aception = cleaned_aception[1:]

        cleaned_aception = " " + cleaned_aception + " "
        cleaned_traintext = " " + cleaned_traintext + " "
        len_traintext: int = len(cleaned_traintext)

        # Chequear Parentesis
        did_have_parenthesis: bool = False
        did_have_slash: bool = False
        splited_word: str = cleaned_aception.split("(")
        extra: str = ""
        splited_extra: list = []
        if (len(splited_word) > 1):
            did_have_parenthesis = True
            cleaned_aception = splited_word[0]
            extra = splited_word[1][:-2]

            # Chequear si el parentesis viene con slash
            splited_extra = extra.split("/")
            if (len(splited_extra) > 1):
                did_have_slash = True

        # print(f"base: {cleaned_aception}, extra: {splited_extra}")

        # Se recorre la palabra por el traintext
        for word_position in range(len_traintext + len(cleaned_aception)):
            is_word_matching: bool = True
            chars_matched: int = 0

            # print("------------")

            # Se recorre cada letra de la acepción
            # (cleaned_aception es la base de la acepcion)
            word: str = cleaned_aception
            char_pos_aception: int = -1
            while True:
                char_pos_aception += 1
                # La posicion del caracter evaluado en el traintext
                char_pos_traintext = char_pos_aception + word_position -\
                    len(cleaned_aception)

                # Chequear limites de acepcion y traintext:
                if (char_pos_traintext < 0):
                    is_word_matching = False
                    continue
                elif (char_pos_aception >= len(word)):
                    # print(f"End of word: {word}")
                    if is_word_matching:
                        if (did_have_parenthesis):
                            if (did_have_slash):
                                if (word == cleaned_aception):
                                    word = cleaned_aception + splited_extra[0]
                                    word = word + " "
                                    splited_extra.pop(0)
                                    char_pos_aception -= 1
                                    continue
                                else:
                                    # print("Slash Match!")
                                    self.didItMatch = True
                                    break
                            else:
                                if (word == cleaned_aception):
                                    word = word + " "
                                    char_pos_aception -= 1
                                    continue
                                else:
                                    # print("Parenthesis Match!")
                                    self.didItMatch = True
                                    break
                        else:
                            # print("Simple Match!")
                            self.didItMatch = True
                            break
                    elif (word != cleaned_aception and len(splited_extra) > 0):
                        word = cleaned_aception + splited_extra[0]
                        word = word + " "
                        splited_extra.pop(0)
                        char_pos_aception = len(cleaned_aception) - 1
                        is_word_matching = True
                        continue
                    else:
                        break
                elif (char_pos_traintext >= len_traintext):
                    if (did_have_slash and
                            word != cleaned_aception and
                            len(splited_extra) > 0):
                        word = cleaned_aception + splited_extra[0]
                        word = word + " "
                        splited_extra.pop(0)
                        char_pos_aception = len(cleaned_aception) - 1
                        is_word_matching = True
                        continue
                    elif (did_have_parenthesis and
                          word != cleaned_aception and
                          extra != ""):
                        word = word[:-1] + extra + " "
                        is_word_matching = True
                        extra = ""
                        continue
                    else:
                        break

                traintext_char: str = cleaned_traintext[char_pos_traintext]
                word_char: str = word[char_pos_aception]

                if (self.AreTheSameChar(
                        traintext_char=traintext_char,
                        word_char=word_char
                        )):
                    chars_matched += 1
                else:
                    is_word_matching = False

                # print(f"{traintext_char} = {word_char}  {is_word_matching}")
                # print(self.didItMatch)

            self.mostCharsMatched = max(self.mostCharsMatched, chars_matched)

    def AreTheSameChar(self, traintext_char, word_char):
        are_the_same_char: bool = False
        if traintext_char == word_char:
            are_the_same_char = True
        elif word_char == "@":
            if traintext_char == "A" or traintext_char == "O":
                are_the_same_char = True
        return are_the_same_char
