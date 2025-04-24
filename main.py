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

print(get_code(generate_response(generate_prompt()))[0])