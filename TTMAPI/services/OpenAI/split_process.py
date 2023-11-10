from TTMAPI.helpers.merge_results import merge_results
from .gpt_process import gpt_process
from .split_in_phrases import split_in_phrases


def create_empty_results(drivers):
    results = {}
    for driver in drivers:
        results[driver.id] = {}
        for component in driver.components:
            results[driver.id][component.id] = 0
    return results


def split_process(answer: str, model: str, drivers, logger):
    final_result = create_empty_results(drivers)
    # Procesa cada frase por separado
    phrases = split_in_phrases(text=answer, logger=logger)
    for phrase in phrases:
        phrase_result, exception = gpt_process(
            answer=phrase,
            drivers=drivers,
            model=model,
            logger=logger)
        if exception:
            logger.error(f"Error con GPT. Error: {exception}")
            continue
        for driver in phrase_result:
            for component in phrase_result[driver]:
                final_result[driver][component] = merge_results(
                    final_result[driver][component],
                    phrase_result[driver][component])
    # Procesa el texto completo y se lo suma a cada componente, como una frase
    total_result, exception = gpt_process(
        answer=answer,
        drivers=drivers,
        model=model,
        logger=logger)
    if exception:
        logger.error(f"Error con GPT. Error: {exception}")
    for driver in total_result:
        for component in total_result[driver]:
            final_result[driver][component] = merge_results(
                final_result[driver][component],
                total_result[driver][component])

    logger.debug(f"final_result = {final_result}")
    return final_result
