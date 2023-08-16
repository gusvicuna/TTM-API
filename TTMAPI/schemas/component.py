def componentSchema(item) -> dict:
    return {
        "name": item.name,
        "phrases": item.phrases,
        "description": item.description
    }


def matchedComponentSchema(item) -> dict:
    return {
        "name": item.name,
        "phrases": item.phrases,
        "description": item.description,
        "bestCharPercent": item.bestCharPercent,
        "mostCharsMatched": item.mostCharsMatched,
        "matchedAceptions": item.matchedAceptions,
        "aceptions": item.aceptions,
        "ttm_result": item.ttm_result,
        "gpt_result": item.gpt_result
    }


def componentsSchema(entity) -> list:
    return [componentSchema(item) for item in entity]


def matchedComponentsSchema(entity) -> list:
    return [matchedComponentSchema(item) for item in entity]
