from config import   config
from openai import OpenAI


def prompt_template():
    return """You are a Business and Data analyst assistant in converting questions asked in plain English language into mathematical and data driven answers with summary
        Here are the details you'll need:
        
        The data retrieved from the in tabular format
        {data_df}
        
        Instructions:
        1. Return Summarised data
        2. USe the websites livemint and Bloomberg to access recent sentiments to provide events and news for the commodity asked
        
        
        Your Task:
        Based on the given dataframe, English question, and urls on internet, present the summary  for a business user.
        English Question: {question}"""


def create_prompt(prompt_template, data_df, question):
    prompt = prompt_template.format(data_df=data_df, question=question)
    return prompt


client = OpenAI(api_key=config['api_key'])  # Pass the API key here


def generate_response(prompt_final):
    try:
        response = client.chat.completions.create(model="gpt-4o",
              messages=[{"role": "user", "content": prompt_final}
            ,{"role": "user", "content": 'Use the data from data_df input only'}
            ,{"role": "user", "content": 'create the final output in well formatted HTML'}])
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
