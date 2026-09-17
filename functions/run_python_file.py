import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_run_abs = os.path.abspath(working_directory)
        target_run = os.path.normpath(os.path.join(working_run_abs, file_path))

        valid_target_dir = os.path.commonpath([working_run_abs, target_run]) == working_run_abs

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_run):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # building the command list
        command = ["python", target_run]

        if args:
            command.extend(args)

        results = subprocess.run(command, capture_output=True,  text=True, timeout=30, cwd=working_run_abs)

        output = []
        if results.returncode:
            output.append(f"Process exited with code {results.returncode}")


        if not results.stdout and not results.stderr:
            output.append("No output produced")

        if results.stdout:
            output.append(f"STDOUT: {results.stdout}")

        if results.stderr:
            output.append(f"STDERR: {results.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: {e}"


# tells the LLM how the function should be called
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "makes sure it is a python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file, relative to the working directory.",
                },
                "args":{
                    "type": "array",
                    "items": {
                        "type":"string"
                    },
                    "description": "a list of command-line arguments to pass to the script when running it"
                },
            },
        },
    },
}