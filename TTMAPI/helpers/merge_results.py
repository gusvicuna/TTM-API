def merge_results(result1: int, result2: int):
    if result1 == 1:
        if result2 == -1 or result2 == 2:
            return 2
        else:
            return 1
    elif result1 == -1:
        if result2 == 1 or result2 == 2:
            return 2
        else:
            return -1
    elif result1 == 2:
        return 2
    else:
        return result2
