from pydantic import BaseModel


class Aception(BaseModel):

    text: str
    bestWordPercent: int = 0
    bestCharPercent: int = 0

    def __str__(self) -> str:
        return f"{self.text}"

    def Words(self):
        return self.text.split(" ")

    def Characters(self):
        return list(str(self.text))

    def CountCharactersWithoutSpaces(self) -> int:
        splited_text = [i for i in self.Characters() if i != " "]
        return len(splited_text)

    def MatchTrainText(self, trainText) -> None:
        aception_char_count = len(self.Characters())
        train_text_char_count = len(trainText.Characters())

        train_id = 0
        while train_id < aception_char_count + train_text_char_count:
            char_match_count = 0
            word_match_count = 0
            word_match = True

            char_id = 0
            while char_id < train_text_char_count:

                moving_aception_id =\
                    aception_char_count - train_id + char_id
                if moving_aception_id < 0 or moving_aception_id >=\
                        aception_char_count:
                    moving_char = ""
                else:
                    moving_char =\
                        self.Characters()[moving_aception_id]

                is_char_an_space = trainText.Characters()[char_id] == " "
                is_final_char = char_id == train_text_char_count - 1
                is_same_char =\
                    trainText.Characters()[char_id] == moving_char
                if is_char_an_space or is_final_char:
                    if word_match:
                        word_match_count += 1
                    word_match = True

                elif is_same_char and moving_char != "":
                    char_match_count += 1
                else:
                    word_match = False

                char_id += 1

            matchedWordsPercent =\
                round(100 * word_match_count / len(self.Words()))
            matchedCharsPercent =\
                100 * char_match_count / self.CountCharactersWithoutSpaces()

            if matchedWordsPercent > self.bestWordPercent:
                self.bestWordPercent = round(matchedWordsPercent, 2)
            if matchedCharsPercent > self.bestCharPercent:
                self.bestCharPercent = round(matchedCharsPercent, 2)

            train_id += 1
