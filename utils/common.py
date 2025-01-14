def load_prompt(file_path) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        template = file.read()
    return template
