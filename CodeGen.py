#Заменить на что угодно
from ollama import chat
from ollama import ChatResponse

MODEL = "yandex/YandexGPT-5-Lite-8B-instruct-GGUF"

def set_model(model_name):
    global MODEL
    MODEL = model_name

def generate_response(prompt, model_name=MODEL):
    response: ChatResponse = chat(model=model_name, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response.message.content

# Сама программа
import re
import subprocess
import argparse

INPUT_DATA_PATH = 'data.html'
OUTPUT_DATA_PATH = 'data.json'


def set_input_data_path(path):
    global INPUT_DATA_PATH
    INPUT_DATA_PATH = path

def set_output_data_path(path):
    global OUTPUT_DATA_PATH
    OUTPUT_DATA_PATH = path

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

def generate_prompt():
    input_data = read_file(INPUT_DATA_PATH)
    output_data = read_file(OUTPUT_DATA_PATH)
    prompt = f"Generate python code that takes Input_Data as input and returns Output_Data to console, also generate requirements.txt like \n```requirements.txt\n...```\n and input data should be readed from file data.html.\nInput_Data: ```{input_data}```\nOutput_Data: ```{output_data}```"
    return prompt

def generate_correction_prompt(script_code, error_message, actual_output):
    input_data = read_file(INPUT_DATA_PATH)
    output_data = read_file(OUTPUT_DATA_PATH)
    prompt = f"Correct the following python code that takes Input_Data as input and returns Output_Data to console, also generate requirements.txt like ```requirements.txt\n...```, Actual_Output should should be consistent with Output_Data.\nInput_Data: ```{input_data}```\nOutput_Data: ```{output_data}```\nError: {error_message}\nActual_Output: {actual_output}\nCode: ```python\n{script_code}```"
    return prompt

def get_code(responce):
    pattern = r"(?s)(?:```python\s*\n?|```\s*\n?)(.*?)\n?```"
    
    code_blocks = re.findall(pattern, responce)

    return [block.strip() for block in code_blocks]

def get_requirements(responce):
    pattern = r"(?s)```requirements\.txt\s*\n(.*?)\n```"
    
    requirements_blocks = re.findall(pattern, responce)

    return [block.strip() for block in requirements_blocks]

def script_save(code):
    with open("script.py", "w") as file:
        file.write(code)

def requirements_save(requirements):
    with open("requirements.txt", "w") as file:
        file.write(requirements)

def docker_run():
    subprocess.run(["sudo", "docker", "build", "-t", "my-python-script", "."])
    result = subprocess.run(["sudo", "docker", "run", "--rm", "my-python-script"], capture_output=True, text=True)

    return result.stdout, result.stderr

def compare_output(script_output, expected_output):
    return script_output.strip() == expected_output.strip()

def commit_changes():
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "#SCRIPT\nUpdate script and requirements"])
    #subprocess.run(["git", "push"])

def start(commit=False):
    script_code = ''
    error_output = ''
    script_output = ''
    prompt = generate_prompt()
    response = generate_response(prompt)
    code_blocks = get_code(response)
    requirements_blocks = get_requirements(response)
    while True:
        if requirements_blocks:
            requirements_save(requirements_blocks[0])
        else:
            print("No requirements found in the response.")

        if code_blocks:
            script_code = code_blocks[0]
            script_save(script_code)
            if commit:
                commit_changes()

            script_output, error_output = docker_run()

            if error_output:
                print(f"Error: {error_output}")
            else:
                expected_output = read_file(OUTPUT_DATA_PATH)
                if compare_output(script_output, expected_output):
                    print("Output matches the expected output.")
                    break # Работает до входа в этот блок
                else:
                    print("Output does not match the expected output.")
        else:
            print("No code blocks found in the response.")
        
        prompt = generate_correction_prompt(script_code, error_output, script_output)
        response = generate_response(prompt)
        code_blocks = get_code(response)
        requirements_blocks = get_requirements(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CodeGen script")
    parser.add_argument("--model", type=str, default="yandex/YandexGPT-5-Lite-8B-instruct-GGUF", help="Name of the ollama model to use")
    parser.add_argument("--input", type=str, default=INPUT_DATA_PATH, help="Path to the input data file")
    parser.add_argument("--output", type=str, default=OUTPUT_DATA_PATH, help="Path to the output data file")
    args = parser.parse_args()
    MODEL = args.model
    start()
