from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

from collections.abc import Callable

import json


available_functions = [
    schema_get_files_info,
    schema_get_files_content,
    schema_run_python_file,
    schema_write_file
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
    # etc.
}

# handle the abstract task of calling one of our four functions and returning its result

def call_function(tool_call, verbose: bool = False) -> dict:
    # Parse function_name and function_args from the tool call.
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    #Print a verbose or brief message depending on the flag.
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    #Bail out early with an error tool message if the function name isn't recognized.
    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    #Inject working_directory into the args.
    function_args["working_directory"] = "./calculator"

    #Call the real function via the map, unpacking args as keywords.
    result = function_map[function_name](**function_args)

    #Return the successful tool message with the result.
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
