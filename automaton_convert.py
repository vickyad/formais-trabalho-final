'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte

    Alunos: Bruno Zimmermann, Jordi Pujol e Victoria Duarte
'''

import re
from typing import NamedTuple, Dict, List
from io import StringIO

class TransitionInput(NamedTuple):
    state: str
    symbol: str

class Transition(NamedTuple):
    input: TransitionInput
    output: str

class Automaton(NamedTuple):
    states: List[str]
    alphabet: List[str]
    prog_function: Dict[TransitionInput, str]
    initial: str
    finals: List[str]

'''
    read_automaton: String -> (List, Dict)
    Lê um arquivo de texto passado no parametro e retorna um par de listas, na ordem
    definition: Lista com a quadrupla de definição separada
    transitions: Dicionário onde:
        chave -> transição no formato (estado,simbolo)
        valor -> estado resultante
'''
def read_automaton(automaton_name: str) -> Automaton:
    # Abre o arquivo contendo o AF
    with open(automaton_name, 'r', encoding='utf8') as machine:

        line = machine.readline().strip()
        prog_name = machine.readline().strip()
        definition_pieces = split_definition(line, prog_name)
        states = definition_pieces[0].split(',')
        alphabet = definition_pieces[1].split(',')
        initial = definition_pieces[2]
        finals = definition_pieces[3].split(',')

        # Lê as linhas de transições e armazena em um dict, na forma
        # {transição : estado_novo}
        # EX:{('q0', 'a'): 'q1', ('q0', 'b'): 'q2', 
        #     ('q3', 'a'): 'q3', ('q3', 'b'): 'q2'}
        prog_function = make_prog_function(machine)

        return Automaton(
                states=states,
                alphabet=alphabet,
                prog_function=prog_function,
                initial=initial,
                finals=finals)

def split_definition(line: str, prog_name: str) -> List[str]:
    prog_name = ',{},'.format(prog_name)
    line = line[0:-1]
    line = line.replace('AUTÔMATO=(', '').replace(',{', '|')
    line = line.replace(prog_name, '|').replace('{', '').replace('}', '')
    return line.split('|')

def make_prog_function(machine: StringIO) -> Dict[TransitionInput, str]:
    transitions = {}
    for line in machine:
        transition = get_transition(line)
        transitions[transition.input] = transition.output
    return transitions

'''
    get_transition: String -> Tuple
    Le uma transição dada em uma string e retorna uma dupla na forma
    (transição, estado)
    EX: '(q0,a)=q1\n' -> ( (q0,a), 'q1' )
'''
def get_transition(line: str) -> Transition:
    input_str, output_str = line.replace('\n', '').split('=')
    pieces = input_str.replace('(', '').replace(')', '').split(',')
    state, symbol = tuple(pieces)
    trans_input = TransitionInput(state=state, symbol=symbol)

    return Transition(input=trans_input, output=output_str)
