import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sqlparse
from schemas.sqldb_schemas import prompt, prompt1
from config import config
# from app import cache


def load_tokenizer():
    # if cache.get('tokenizer') is not None:
    #     return cache['tokenizer']
    tokenizer = AutoTokenizer.from_pretrained(config['model_name'])
    # cache['tokenizer'] = tokenizer
    return tokenizer


def load_model():
    # if cache.get('model') is not None:
    #     print('Loading model from cache')
    #     return cache.get('model')

    # Check if GPU is available?
    available_memory = 1e6 # TODO : Remove this
    # available_memory = torch.cuda.get_device_properties(0).total_memory
    print(torch.cuda.is_available(), available_memory)
    """##Download the Model
    Use any model on Colab (or any system with >30GB VRAM on your own machine) to load this in f16.
     If unavailable, use a GPU with minimum 8GB VRAM to load this in 8bit, or with minimum 5GB of VRAM to load in 4bit.
    
    This step can take around 5 minutes the first time. So please be patient :)
    """
    print('started loading model')
    if available_memory > 16e9:
        # if you have at least 15GB of GPU memory, run load the model in float16
        model = AutoModelForCausalLM.from_pretrained(
            config['model_name'],
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=True,
        )
    else:
        # else, load in 8 bits – this is a bit slower
        model = AutoModelForCausalLM.from_pretrained(
            config['model_name'],
            trust_remote_code=True,
            # torch_dtype=torch.float16,
            load_in_8bit=True,
            device_map="auto",
            use_cache=True,
        )
    print('finished loading model')
    # cache['model'] = model
    return model


def generate_query(question):
    tokenizer = load_tokenizer()
    updated_prompt = prompt.format(question=question)
    # updated_prompt = prompt1.format(question=question)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = tokenizer(updated_prompt, return_tensors="pt").to(device)
    generated_ids = load_model().generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=1,
    )
    outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    # empty cache so that you do generate more results w/o memory crashing
    # particularly important on Colab – memory management is much more straightforward
    # when running on an inference service
    return sqlparse.format(outputs[0].split("[SQL]")[-1], reindent=True)



import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

def load_model1():

    # Initialize the tokenizer from Hugging Face Transformers library
    tokenizer = T5Tokenizer.from_pretrained('t5-small')

    # Load the model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql')
    model = model.to(device)
    model.eval()
    return model, tokenizer


def generate_query1(input_prompt):
    model, tokenizer = load_model1()
    # Tokenize the input prompt
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)

    # Forward pass
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)

    # Decode the output IDs to a string (SQL query in this case)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_sql
