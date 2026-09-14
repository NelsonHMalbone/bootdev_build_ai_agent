import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))


        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            results = []
            items = os.listdir(target_dir)
            for item in items:
                file_name = os.path.join(target_dir, item)
                file_name_results = os.path.getsize(file_name)
                results.append(f'- {item}: file_size={file_name_results} bytes, is_dir={os.path.isdir(file_name)}')

            return "\n".join(results)

    except Exception as e:

        return f"Error: {e}"


# tells the LLM how the function should be called

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}