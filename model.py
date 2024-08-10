import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sqlparse
from schemas.sqldb_schemas import prompt
from app import cache
from flask import current_app as app


def load_tokenizer():
    if cache.get('tokenizer') is not None:
        return cache['tokenizer']
    tokenizer = AutoTokenizer.from_pretrained(app.config['model_name'])
    cache['tokenizer'] = tokenizer
    return tokenizer


def load_model():
    if cache.get('model') is not None:
        print('Loading model from cache')
        return cache.get('model')

    # Check if GPU is available?
    available_memory = torch.cuda.get_device_properties(0).total_memory
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
            app.config['model_name'],
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=True,
        )
    else:
        # else, load in 8 bits – this is a bit slower
        model = AutoModelForCausalLM.from_pretrained(
            app.config['model_name'],
            trust_remote_code=True,
            # torch_dtype=torch.float16,
            load_in_8bit=True,
            device_map="auto",
            use_cache=True,
        )
    print('finished loading model')
    cache['model'] = model
    return model


def generate_query(question):
    tokenizer = load_tokenizer()
    updated_prompt = prompt.format(question=question)
    inputs = tokenizer(updated_prompt, return_tensors="pt").to("cuda")
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
