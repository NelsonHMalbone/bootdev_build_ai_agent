import os
import json
import argparse

from prompts import system_prompt
from call_function import available_functions, call_function

from dotenv import load_dotenv
from openai import OpenAI



def main():
    print("Hello from build-ai-agent!")
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("ran out of time for apikey")

    client = OpenAI(base_url='https://openrouter.ai/api/v1',
                    api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,

    )

    if response.usage is None:
        raise RuntimeError("ran out of time for response usage")
    else:
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    #print(response.choices[0].message.content)
    message = response.choices[0].message

    if message.tool_calls is None:
        print(message.content)
    else:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            # checks if empty or missing, and stops the program with an error
            if not result_message["content"]:
                raise Exception("no content returned")

            # only prints the actual result content when --verbose is passed
            if args.verbose:
                print(f"-> {result_message['content']}")

if __name__ == "__main__":
    main()
