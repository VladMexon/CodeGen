#Заменить на что угодно
from google import genai
client = genai.Client(api_key="AIzaSyA9M9pYa84TV6kbTn8LFVIdrLB7qBdlYOY")

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

# Сама программа
import re

INPUT_DATA_PATH = 'data.html'
OUTPUT_DATA_PATH = 'data.json'

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

def generate_prompt():
    input_data = read_file(INPUT_DATA_PATH)
    output_data = read_file(OUTPUT_DATA_PATH)
    prompt = f"Generate python code that takes Input_Data as input and returns Output_Data to console.\nInput_Data: ```{input_data}```\nOutput_Data: ```{output_data}```"
    return prompt

def get_code(responce):
    pattern = r"(?s)(?:```python\s*\n?|```\s*\n?)(.*?)\n?```"
    code_blocks = re.findall(pattern, responce)

    return [block.strip() for block in code_blocks]

def script_save(code):
    with open("script.py", "w") as file:
        file.write(code)

def docker_run():
    import subprocess
    subprocess.run(["docker", "build", "-t", "my-python-script", "."])
    result = subprocess.run(["docker", "run", "--rm", "my-python-script"], capture_output=True, text=True)

    return result.stdout, result.stderr

def compare_output(script_output, expected_output):
    return script_output.strip() == expected_output.strip()

def main():
    prompt = generate_prompt()
    response = generate_response(prompt)
    code_blocks = get_code(response)

    if code_blocks:
        script_code = code_blocks[0]
        script_save(script_code)

        script_output, error_output = docker_run()

        if error_output:
            print(f"Error: {error_output}")
        else:
            expected_output = read_file(OUTPUT_DATA_PATH)
            if compare_output(script_output, expected_output):
                print("Output matches the expected output.")
            else:
                print("Output does not match the expected output.")
    else:
        print("No code blocks found in the response.")

if __name__ == "__main__":
    main()
