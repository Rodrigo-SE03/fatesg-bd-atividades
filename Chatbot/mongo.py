import pandas as pd
import pymongo  # Para interagir com o banco de dados MongoDB


# Conectando ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["chatbot"]
collection = db["funcionarios"]


funcionarios = []
with open('Chatbot\Salary Data copy.csv', 'r') as f:
    for line in f.readlines()[1:70]:
        line = line.split(',')
        funcionario = {
            "idade": int(line[0]),
            "genero": line[1],
            "escolaridade": line[2],
            "cargo": line[3],
            "experiencia": line[4],
            "salario": float(line[5].replace(',', '.'))/10, # O valor foi dividido por 10 pois estava muito alto
        }
        funcionarios.append(funcionario)

# Inserindo no MongoDB
collection.insert_many(funcionarios)
print("Dados inseridos com sucesso!")


