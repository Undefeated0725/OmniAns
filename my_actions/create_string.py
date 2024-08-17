from aijson import register_action

@register_action
def create_string(string: str) -> str:
    print(string)
    return string
