from model import generate_query
from openai_api import create_prompt, prompt_template, generate_response
from sql_connection import read_sql

# question = "select average forecast prices for corn for Jan 2024"

def aisearch(question:str):
    generated_sql = generate_query(question)
    data_df = read_sql(generated_sql)
    prompt_final = create_prompt(prompt_template(), data_df, question)
    return generate_response(prompt_final)
