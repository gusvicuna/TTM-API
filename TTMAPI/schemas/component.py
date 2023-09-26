from TTMAPI.models.component import Component


def createComponentSchema(item: Component) -> dict:
    return {
        "name": item.name,
        "phrases": item.phrases,
        "description": item.description
    }


def getComponentSchema(item: Component) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "phrases": item.phrases,
        "description": item.description
    }


def getMatchedComponentSchema(item: Component) -> dict:
    return {
        "id": item.id,
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


def createComponentsSchema(entity) -> list:
    return [createComponentSchema(item) for item in entity]


def getComponentsSchema(entity) -> list:
    return [getComponentSchema(item) for item in entity]


def getMatchedComponentsSchema(entity) -> list:
    return [getMatchedComponentSchema(item) for item in entity]
