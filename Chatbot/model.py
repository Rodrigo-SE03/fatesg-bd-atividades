import pymongo 
import torch
from transformers import AutoTokenizer, Gemma3ForCausalLM
torch.classes.__path__ = [] 
# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["chatbot"]  
collection = db["conversas"]
docs = db['funcionarios']

ckpt = "google/gemma-3-1b-it"
model = Gemma3ForCausalLM.from_pretrained(
    ckpt, torch_dtype=torch.bfloat16, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(ckpt)

messages = []

def get_docs():
    documents = docs.find()
    return documents

def get_conversas():
    conversas = collection.find()
    return conversas

def limpar_historico():
    collection.delete_many({})


def gerar_resposta(pergunta):
    if pergunta.strip() == '': return ''
    messages.append({"role": "user", "content": pergunta})
    for m in messages:
        print(m)
    
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True,
        return_dict=True, return_tensors="pt"
    ).to(model.device)
    input_len = inputs["input_ids"].shape[-1]
    generation = model.generate(**inputs, max_new_tokens=300, do_sample=False)
    generation = generation[0][input_len:]

    decoded = tokenizer.decode(generation, skip_special_tokens=True)
    messages.append({"role": "assistant", "content": decoded})

    collection.insert_one({
        "pergunta": pergunta,
        "resposta": decoded
    })
    return decoded

messages.append({"role": "system", "content": "Você é um assistente útil."})
msg = 'Essa é a lista de funcionários da empresa:'

cols = ['nome', 'idade', 'email', 'telefone', 'cargo', 'salario', 'setor']

msg += '\n' + ', '.join(cols)
for d in get_docs():
    msg += '\n'
    for c in cols:
        msg += str(d[c]) + ','
    msg = msg[:-1]
    
messages.append({"role": "user", "content": msg})
messages.append({"role": "system", "content": "Okay, vou usar essa lista para te ajudar com o que precisar."})
# Colocar as conversas do banco de dados na variável messages
for conversa in get_conversas():
    messages.append({"role": "user", "content": conversa["pergunta"]})
    messages.append({"role": "assistant", "content": conversa["resposta"]})

