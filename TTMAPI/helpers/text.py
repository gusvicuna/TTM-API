def LenOfCharsWithoutSpace(text: str):
    splited_text = [i for i in list(text) if i != " "]
    return len(splited_text)


def BiggestWord(text: str):
    biggest_word = ""
    for word in text.split(" "):
        if len(word) > len(biggest_word):
            biggest_word = word
    return biggest_word


def Clean(text: str) -> str:
    text = text.replace("á", "a")
    text = text.replace("é", "e")
    text = text.replace("í", "i")
    text = text.replace("ó", "o")
    text = text.replace("ú", "u")
    text = text.replace(".", "")
    text = text.upper()
    return text
