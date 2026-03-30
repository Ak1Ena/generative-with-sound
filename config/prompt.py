import json
import os

# Get the directory of the current file (config/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# The action.json is in the parent directory (project root)
action_path = os.path.join(current_dir, "..", "action.json")

with open(action_path, "r") as f:
    action_json = json.load(f)

# Filter action_json to remove implementation details (function, location)
ai_actions = []
for action in action_json:
    ai_actions.append({
        "name": action.get("name"),
        "description": action.get("description"),
        "args": action.get("args")
    })

prompt = f"""
    You are the human not AI.

    Available actions which you can use:
    {json.dumps(ai_actions, indent=2)}

    How to use:
    - for send action you have to use [**action_name<arg1=val1,arg2=val2>**]
    - for action without args you can use [**action_name**]
    - the action have to be at the end of sentences.
"""

