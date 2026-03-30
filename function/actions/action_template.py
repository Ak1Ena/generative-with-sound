"""
RinneAI Action Template
Use this as a starting point for creating new actions.
"""

async def action_handler_template(args, callback):
    """
    Standard signature for all RinneAI actions.
    
    Args:
        args (dict): Dictionary of arguments passed from the AI 
                     e.g., [**action<x=1,y=2>**] -> {'x': '1', 'y': '2'}
        callback (function): The process_interaction function. Use this if 
                             the action needs to send a response or image back to the AI.
    """
    # 1. Extract your arguments (they come in as strings from the parser)
    # example_arg = args.get('key', 'default_value')

    print(f"--- Executing Action Template ---")

    # 2. Implement your logic here (e.g., file system, web search, mouse control)
    # ... logic ...

    # 3. (Optional) Provide feedback to the AI
    # This triggers the AI to speak the result or analyze a new state.
    # await callback("I have finished the task. Here is what happened...", image=None)
    pass
