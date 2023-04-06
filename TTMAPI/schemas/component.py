def componentSchema(item) -> dict:
    return {
        "name": item.name,
        "phrases": item.phrases
    }


def matchedComponentSchema(item) -> dict:
    return {
        "name": item.name,
        "phrases": item.phrases,
        "bestWordPercent": item.bestWordPercent,
        "bestCharPercent": item.bestCharPercent,
        "mostWordsMatched": item.mostWordsMatched,
        "mostCharsMatched": item.mostCharsMatched,
    }


def componentsSchema(entity) -> list:
    return [componentSchema(item) for item in entity]


def matchedComponentsSchema(entity) -> list:
    return [matchedComponentSchema(item) for item in entity]
