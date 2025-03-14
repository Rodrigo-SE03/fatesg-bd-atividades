import pymongo  # Para interagir com o banco de dados MongoDB
import requests
import random
import numpy as np

def gerar_salario(idade):
    coeficiente = 1500 
    intercepto = 0
    salario_base = intercepto + coeficiente * idade
    ruido = np.random.normal(0, 10000)
    
    return round(salario_base + ruido, 2)

# Conectando ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["chatbot"]
collection = db["funcionarios"]


url = "https://randomuser.me/api/?results=20&nat=br"


# Fazemos uma requisição GET para a API e obtemos os dados no formato JSON
response = requests.get(url).json()


# Criamos uma lista para armazenar os funcionários processados antes de inseri-los no MongoDB
funcionarios = []

# Percorremos cada usuário retornado pela API
for user in response["results"]:
    # Extraímos os dados necessários e organizamos em um dicionário
    funcionarios.append({
        "nome": f"{user['name']['first']} {user['name']['last']}",  # Nome completo do funcionário
        "idade": user["dob"]["age"],  # Idade
        "email": user["email"],  # Endereço de e-mail
        "telefone": user["phone"],  # Número de telefone
        # Definição do cargo com base na idade: abaixo de 30 anos é "Desenvolvedor", senão "Gerente"
        "cargo": "Desenvolvedor" if user["dob"]["age"] < 30 else "Gerente",
        # Definição do salário com base no cargo: Desenvolvedor recebe R$ 7.000 e Gerente recebe R$ 12.000
        "salario": gerar_salario(user["dob"]["age"]),
        "setor": "TI"  # Setor padrão para todos os funcionários
    })
collection.insert_many(funcionarios)
print("Dados inseridos com sucesso!")


