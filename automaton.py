'''
TRABALHO FINAL
LINGUAGENS FORMAIS E AUTOMATOS - 2020
Prof. Lucio Duarte

Alunos: Bruno Zimmermann, Jordi Pujol e Victoria Duarte
'''

import re
from typing import NamedTuple, Dict, List, TextIO

class TransitionInput(NamedTuple):
    '''
    A entrada de uma transição, passada para a função programa. Por exemplo,
    "(q0, a)" é a entrada da chamada "delta(q0, a)".

    O Campo 'state' é o estado atual e corresponde a "q0" no exemplo acima.

    O Campo 'symbol' é o símbolo para o qual a fita aponta, e corresponde a "a"
    no exemplo acima.
    '''

    state: str
    symbol: str

class Transition(NamedTuple):
    '''
    Uma transição completa, com entrada e saída. Usado somente na função
    make_transition. O autômato guarda entrada e saída de uma transição
    separadamente, portanto, não usa esta classe. Corresponde à expressão
    no formato "delta(q0, a) = q1".

    O campo 'input' é uma entrada da função programa. Corresponde a "(q0, a)" no
    exemplo acima.

    O campo 'output' é o novo estado e a saída da função programa. Corresponde a
    "q1" no exemplo acima.
    '''

    input: TransitionInput
    output: str

class Automaton(NamedTuple):
    '''
    Um autômato finito determinístíco.

    O campo 'states' lista o nome de todos os estados, inclusive os estados
    inicial e finais.

    O campo 'alphabet' lista todos os símbolos que a linguagem reconhecida pelo
    autômato usa.

    O campo 'prog_function' lista as transições possíveis. É a função programa
    no formato de um dicionário, onde a chave do dicionário é o par
    "estado atual" e "símbolo atual", que são mapeados para um novo estado. Ou
    seja, o formato deste campo é: "(q0, a) -> q1".

    O campo 'initial' define qual é o estado inicial.

    O campo 'finals' lista quais são os estados considerados finais.
    '''

    states: List[str]
    alphabet: List[str]
    prog_function: Dict[TransitionInput, str]
    initial: str
    finals: List[str]

def read_automaton(automaton_path: str) -> Automaton:
    '''
    Lê um arquivo de texto passado no parametro e retorna o autômato definido no
    arquivo. O caminho do arquivo é definido pelo parâmetro 'automaton_path'.
    '''

    # Abre o arquivo contendo o AF
    with open(automaton_path, 'r', encoding='utf8') as machine_file:

        # Linha inicial de definições, com espaços em branco no início e no fim
        # da linha removidos.
        line = machine_file.readline().strip()

        # Nome da função programa na linha seguinte.
        prog_name = machine_file.readline().strip()

        # Os componentes da definição do autômato separados.
        definition_pieces = split_definition(line, prog_name)

        # Lista completa de estados no primeiro pedaço.
        states = definition_pieces[0].split(',')
        # Lista completa de símbolos no segundo pedaço.
        alphabet = definition_pieces[1].split(',')
        # Estado inicial no terceiro pedaço.
        initial = definition_pieces[2]
        # Lista completa de estados no quarto pedaço.
        finals = definition_pieces[3].split(',')

        # Lê as linhas restantes, contendo transições.
        prog_function = make_prog_function(machine_file)

        # Instancia o autômato.
        return Automaton(
                states=states,
                alphabet=alphabet,
                prog_function=prog_function,
                initial=initial,
                finals=finals)

def split_definition(line: str, prog_name: str) -> List[str]:
    '''
    Recebe a primeira linha do arquivo de um autômato (o parâmetro 'line'),
    a linha da definição do autômato, e quebra ela em pedaços com o objetivo
    de usar os pedaços para instanciar um autômato.
    '''

    # Vamos eliminar o nome da função programa da definição
    # (não precisamos dela).
    prog_name = ',{},'.format(prog_name)
    # Eliminando o último parêntesis da linha ')'.
    line = line[0:-1]
    # Eliminando o lado esquerdo da definição (não precisamos).
    line = line.replace('AUTÔMATO=(', '')
    # Fazendo com que os elementos da definição sejam separados por '|'.
    line = line.replace(',{', '|').replace(prog_name, '|')
    # Eliminando as chaves.
    line = line.replace('{', '').replace('}', '')
    # Finalmente separando.
    return line.split('|')

def make_prog_function(machine_file: TextIO) -> Dict[TransitionInput, str]:
    '''
    Lê o restante das linhas do arquivo de entrada 'machine_file', onde cada
    linha é uma nova transição.
    '''

    # Inicializando o dicionário de transições.
    transitions = {}
    # Para toda linha restante no arquivo, faça:
    for line in machine_file:
        # Lendo a transição naquela linha.
        transition = make_transition(line)
        # Mapear a entrada da transição para a saída da transição.
        #
        # Isto é, mapear "(q0, a) -> q1".
        transitions[transition.input] = transition.output
    # Retornando as transições.
    return transitions

def make_transition(line: str) -> Transition:
    '''
    Le uma transição dada no parâmetro 'line' e retorna uma transição.

    Exemplo:
        ,make_transition('(q0,a)=q1')
        =
        Transition(TransitionInput('q0', 'a'), 'q1')
    '''
    
    # Remove whitespaces do início e fim, e separa pelo sinal '='.
    #
    # Antes do sinal vem a entrada, e depois a saída.
    input_str, output_str = line.strip().split('=')

    # Remove parêntesis da string da entrada e separa a string por vírgula,
    # em uma lista.
    pieces = input_str.replace('(', '').replace(')', '').split(',')
    # Instancia a entrada da transição.
    trans_input = TransitionInput(state=pieces[0], symbol=pieces[1])

    # Retorna a transição.
    return Transition(input=trans_input, output=output_str)
