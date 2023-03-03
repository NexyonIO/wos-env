def is_tool(name) -> bool:
    from shutil import which
    return which(name) is not None


def ask_user(msg: str, answers: tuple) -> str:
    user_input = ""

    while user_input not in answers:
        user_input = input(msg + f" [{'/'.join(answers)}]: ")
    
    return user_input
