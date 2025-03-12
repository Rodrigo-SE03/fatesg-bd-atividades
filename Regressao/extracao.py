import pandas as pd
import requests  # Para fazer requisições HTTP e obter dados de uma API
import pymongo  # Para interagir com o banco de dados MongoDB


# Conectando ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["startup"]
collection = db["funcionarios"]

# Lendo os dados do CSV
df = pd.read_csv('Salary Data.csv')

# Limpeza dos dados (remoção de valores nulos)
df.dropna(inplace=True)

#  Eliminação de outliers
media = df['Salary'].mean()
desvio = df['Salary'].std()
df = df[df['Salary'] < media + 2*desvio]
df = df[df['Salary'] > media - 2*desvio]

# Inserção dos dados no MongoDB
funcionarios = []

for _, row in df.iterrows():
    funcionario = {
        "idade": int(row["Age"]),
        "genero": row["Gender"],
        "escolaridade": row["Education Level"],
        "cargo": row["Job Title"],
        "experiencia": float(row["Years of Experience"]),
        "salario": float(row["Salary"])/10, # O valor foi dividido por 10 pois estava muito alto
    }
    funcionarios.append(funcionario)

# Inserindo no MongoDB
collection.insert_many(funcionarios)

print("Dados inseridos com sucesso!")