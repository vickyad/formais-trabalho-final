# Abre o arquivo contendo o AF
machine = open('testinho.txt', 'r', encoding='utf8')

# Lê a definição do autômato
definition = machine.readline()
definition = definition.replace(',{', '|{')
definition = definition.replace(',Prog,', '|')
definition = definition.split('|')
print(definition)
# Descarta a linha escrita "Prog"
machine.readline()

# Lê as transições
transitions = []
for l in machine:
    transitions.append(l)
print(transitions)

machine.close()

# Seta a transição inicial
node = definition[2]
print(f'S -> {node}')


# AFD -> GR
'''
Primeira parte
    - S -> inicial
        devemos ler a 'quarta parte' da definição
    - finais -> ε (palavra vazia)
        devemos ler a 'quinta parte' da definição
    
Segunda parte
    - (q0,a)=q1 => q0 -> aq1
        cada item do vetor será transformado em uma transição
'''