from model import generate_query, generate_query1
from openai_api import create_prompt, prompt_template, generate_response
from sql_connection import read_sql

# question = "select average forecast prices for corn for Jan 2024"

def aisearch(question:str):
    generated_sql = generate_query(question)
    # generated_sql = generate_query1(question)
    # generated_sql= '''Select outlook_duration,avg(model_output) from forecast_price_master_product
    #                                       where commodity_id = 1014
    #                                       group by outlook_duration '''
    # print('generated_sql:',generated_sql)
    data_df = read_sql(generated_sql)
    print('data_df:',data_df)
    prompt_final = create_prompt(prompt_template(), data_df, question)
    return generate_response(prompt_final)
