import pymongo 
from llama_cpp import Llama

# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["chatbot"]  
collection = db["conversas"]  

model_path = "mistral.gguf" 
llm = Llama(model_path=model_path, n_ctx=2048,verbose=False)
messages = [
        {"role": "system", "content": "Você é um assistente útil."}
    ]

def get_conversas():
    conversas = collection.find()
    return conversas

def limpar_historico():
    collection.delete_many({})

# Colocar as conversas do banco de dados na variável messages
for conversa in get_conversas():
    messages.append({"role": "user", "content": conversa["pergunta"]})
    messages.append({"role": "assistant", "content": conversa["resposta"]})

def gerar_resposta(pergunta):
    messages.append({"role": "user", "content": pergunta})
    response = llm.create_chat_completion(messages=messages, max_tokens=300)
    resp_text = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": resp_text})

    collection.insert_one({
        "pergunta": pergunta,
        "resposta": resp_text
    })
    return resp_text