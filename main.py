'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte

    Alunos: Bruno Zimmerman, Jordi Pujol e Victoria Duarte
'''


''' EXERCICIO 1 '''
''' item a '''
# Cria a matriz de transições
transition_table = []
for i in range(3):
    transition_table.append([])

# Abre o arquivo contendo o AF
machine = open('testinho.txt', 'r', encoding='utf8')

# Lê a definição do autômato
definition = machine.readline()
definition = definition.replace(',{', '|{').replace(',Prog,', '|').split('|')

# Descarta a linha escrita "Prog"
machine.readline()

# Lê as transições
transitions = []
for l in machine:
    transitions.append(l)

# Fecha o arquivo txt
machine.close()

# Seta a transição inicial
transition_table[0].append('S')
transition_table[1].append(definition[2])
transition_table[2].append(-1)

# Seta as transições finais
node_group = definition[3].replace('{', '').replace('})\n', '').split(',')
for node in node_group:
    transition_table[0].append(node)
    transition_table[1].append('ε')
    transition_table[2].append(-1)

# Seta transições intermediárias
for t in transitions:
    transition_table[0].append(t[1:3])
    transition_table[1].append(t[4:5])
    transition_table[2].append(t[7:9])

# Deleta as variáveis auxiliares
del node_group
del transitions
del definition

''' item b '''
# Pegaria a variável do teclado, mas, por hora, a variável é fixa por motivos de teste
# word = input("digite uma palavra: ")
word = 'aba'

word_m = word + 'ε'     # Acrescenta o símbolo de palavra vazia ao final da palavra,
                # para que a gramática possa identificar parada por aceitação

# Sets iniciais
current_state = transition_table[1][0]  # seta o estado inicial
transitions = f'S -> {current_state}'   # inicia as transições realizadas na verificação
interrupt = 0   # flag que indica se a palavra foi aceita ou não (se houve interrupção do laço for
                # mais externo a plavra foi rejeitada. Caso contrário, foi aceita)

# Leitura simbolo a simbolo da palavra
for symbol in word_m:
    # Verificação de cada estado
    for i in range(len(transition_table[0])):
        found = 0   # flag que indica se foi encontrada alguma transição

        # Caso uma transição tenha sido encontrada, ela é adicionada nas transições e estado atual é alterado
        if (transition_table[0][i] == current_state) and (symbol == transition_table[1][i]):
            transitions += f'{transition_table[0][i]} -> {transition_table[1][i]}{transition_table[2][i]}\n'
            current_state = transition_table[2][i]
            found = 1
            break

    if found == 0:
        interrupt = 1
        break

# Print dos resultados obtidos
if interrupt == 1:
    print(f'{word} pertence a REJEITA')
else:
    print(f'{word} pertence a ACEITA')
    print(transitions)
