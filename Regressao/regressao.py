import pymongo
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["startup"]  
collection = db["funcionarios"]  


data = list(collection.find({}, {"_id": 0, "idade": 1, "salario": 1}))  
df = pd.DataFrame(data)  

df.to_csv("funcionarios.csv", index=False)



X = df[["idade"]]
print(X)
y = df["salario"]
print(y)


# Dividimos os dados em conjunto de treino (80%) e conjunto de teste (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  

model = LinearRegression()  
model.fit(X_train, y_train) 


# Testar predições
for idade in range(25, 45, 5):
    salario_predito = model.predict(pd.DataFrame([[idade]], columns=["idade"]))
    print(f"Idade: {idade}, Salário estimado: R$ {salario_predito[0]:.2f}")

#draw the regression line
import matplotlib.pyplot as plt
plt.scatter(X_train, y_train, color = 'red')
plt.plot(X_train, model.predict(X_train), color = 'blue')
plt.title('Idade x Salário (Conjunto de Treino)')
plt.xlabel('Idade')
plt.ylabel('Salário')
plt.show()