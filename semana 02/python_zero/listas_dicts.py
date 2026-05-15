ferramentas = ["nmap", "nikto", "gobuster", "metasploit", "burpsuite"]

print(ferramentas[0])  # Acessa o primeiro elemento
print(len(ferramentas))  # Imprime o número de elementos na lista

ferramentas.append("sqlmap")  # Adiciona um elemento ao final da lista
print(ferramentas)

pessoa ={
    "nome": "john doe",
    "idade": 30,
    "altura": 1.75,
    "estudante": True
}

print(pessoa["nome"])  # Acessa o valor da chave "nome"
print(pessoa["idade"])  # Acessa o valor da chave "idade"
pessoa["email"] = "john.doe@example.com"  # Adiciona uma nova chave-valor
print(pessoa)  # Imprime o dicionário completo