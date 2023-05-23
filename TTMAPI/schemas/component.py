def componentSchema(item) -> dict:
    return {
        "name": item.name,
        "phrases": item.phrases
    }


def matchedComponentSchema(item) -> dict:
    return {
        "name": item.name,
        "phrases": item.phrases,
        "bestCharPercent": item.bestCharPercent,
        "mostCharsMatched": item.mostCharsMatched,
        "matchedAceptions": item.matchedAceptions,
        "aceptions": item.aceptions,
    }


def componentsSchema(entity) -> list:
    return [componentSchema(item) for item in entity]


def matchedComponentsSchema(entity) -> list:
    return [matchedComponentSchema(item) for item in entity]
