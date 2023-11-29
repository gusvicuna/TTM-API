from TTMAPI.helpers.merge_results import merge_results
from TTMAPI.services.OpenAI.gpt_process import gpt_process
from TTMAPI.services.OpenAI.split_in_phrases import split_in_phrases


def create_empty_results(drivers):
    results = {}
    for driver in drivers:
        results[driver.id] = {}
        for component in driver.components:
            results[driver.id][component.id] = 0
    return results


def split_process(
        answer_text: str,
        answer_type: str,
        commerce_type: str,
        model: str,
        drivers,
        logger):
    final_result = create_empty_results(drivers)
    exceptions = []
    # Procesa cada frase por separado
    phrases = split_in_phrases(text=answer_text, logger=logger)
    for phrase in phrases:
        phrase_result, exception = gpt_process(
            answer_text=phrase,
            answer_type=answer_type,
            commerce_type=commerce_type,
            drivers=drivers,
            model=model,
            logger=logger)
        if exception:
            logger.error(f"Error con GPT. Error: {exception}")
            exceptions.append(exception)
            continue
        for driver in phrase_result:
            for component in phrase_result[driver]:
                final_result[driver][component] = merge_results(
                    final_result[driver][component],
                    phrase_result[driver][component])
    # Procesa el texto completo y se lo suma a cada componente, como una frase
    total_result, exception = gpt_process(
        answer_text=answer_text,
        answer_type=answer_type,
        commerce_type=commerce_type,
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

    logger.debug(f"Final result: {final_result}, exceptions: {exceptions}")
    return final_result, exceptions
