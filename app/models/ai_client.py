from openai import OpenAI

def get_openai_client(base_url, api_key):
    return OpenAI(api_key=api_key, base_url=base_url)

def chat_completion(base_url, api_key, model_name, messages, stream=False):
    client = get_openai_client(base_url, api_key)
    if stream:
        return client.chat.completions.create(model=model_name, messages=messages, stream=True)
    else:
        response = client.chat.completions.create(model=model_name, messages=messages)
        return response.choices[0].message.content, response.usage.total_tokens if response.usage else 0
