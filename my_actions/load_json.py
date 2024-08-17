import json
from typing import Any
from aijson import register_action

@register_action
def load_json(json_string: str) -> Any:
    try:
        json_object = json.loads(json_string)
        print(json_object)
    except json.JSONDecodeError as e:
        print("Failed to parse json",
        data=json_string)
        raise ValueError(f"Invalid JSON string: {e}")
    return json_object    

# Example usage:
# inputs = Inputs(json_string='{"key": "value"}')
# action = LoadJSON()
# result = await action.run(inputs)
# print(result.json_object)  # Outputs: {'key': 'value'}