'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte

    Alunos: Bruno Zimmerman, Jordi Pujol e Victoria Duarte
'''

import re

'''
    read_automaton: String -> (List, Dict)
    Lê um arquivo de texto passado no parametro e retorna um par de listas, na ordem
    definition: Lista com a quadrupla de definição separada
    transitions: Dicionário onde:
        chave -> transição no formato (estado,simbolo)
        valor -> estado resultante
'''
def read_automaton(automaton_name):
    # Abre o arquivo contendo o AF
    with open(automaton_name, 'r', encoding='utf8') as machine:

        line = machine.readline()
        definition = make_definition(line)

        # Descarta a linha escrita "Prog"
        machine.readline()

        # Lê as linhas de transições e armazena em um dict, na forma
        # {transição : estado_novo}
        # EX:['(q0,a)=q1\n', '(q0,b)=q2\n', '(q1,b)=q2\n', '(q3,b)=q2']
        transitions = {}
        for l in machine:
            transition, new_state = get_transition(l)
            transitions[transition] = new_state

    return (definition, transitions)


'''
    make_definition: String -> List
    Ao receber uma linha, retorna uma Lista com cada parte da definição parseada
    [ lista_estados, alfabeto, inicial, lista_finais ]
'''
def make_definition(line):
    # Lê a definição do autômato e separa ele em um vetor
    # EX: ['AUTÔMATO=({q0,q1,q2,q3}', '{a,b}', 'q0', '{q1,q3})\n']
    definition = line.replace(',{', '|{').replace(',Prog,', '|').split('|')

    # Na primeira posição, apaga tudos os frufrus e transforma em uma lista separando por ','
    states = definition[0].replace("AUTÔMATO=(", '').replace('{','').replace('}','').split(',')

    # Na segunda, separa o alfabeto da mesma forma
    sigma = definition[1].replace('{','').replace('}','').split(',')

    # Mantem a terceira e na quarta, faz o mesmo que nas anteriores
    finals = definition[3].replace(")\n", '').replace('{','').replace('}','').split(',')

    # Retorna o valor final
    return [ states, sigma, definition[2], finals ]


'''
    get_transition: String -> Tuple
    Le uma transição dada em uma string e retorna uma dupla na forma
    (transição, estado)
    EX: '(q0,a)=q1\n' -> ( (q0,a), 'q1' )
'''
def get_transition(line):
    clean_line = line.replace('\n', '').split('=')
    transition = tuple(clean_line[0].replace('(', '').replace(')', '').split(','))
    return ( transition, clean_line[1] )