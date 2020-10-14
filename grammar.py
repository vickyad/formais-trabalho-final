import string

from typing import NamedTuple, Optional, List, Dict
from automaton_convert import Automaton

# Tipo das saídas das produções. Sempre na forma aA, ou ε na última transição.
class Derivation(NamedTuple):
    terminal: str
    variable: Optional[str]

    # Representação textual.
    def __str__(self):
        if self.variable is None:
            return 'ε'
        return '{}{}'.format(self.terminal, self.variable)

# Saída final de uma produção.
END_OUTPUT: Derivation = Derivation(terminal='', variable=None)

def derivations_to_str(derivations: List[Derivation]) -> str:
    word = ''
    output = ''
    for derivation in derivations:
        word = '{}{}'.format(word, derivation.terminal)
        output = '{}{}{} => '.format(output, word, derivation.variable)
    output = '{}{}'.format(output, word)
    return output

class Grammar:
    productions: Dict[str, List[Derivation]]
    initial: str

    def __init__(self, automaton: Automaton):
        '''
            Dicionario de listas duplas, onde cada valor:
            variavel : lista_produções
            lista_produções : 
                | [ (terminal, variavel), (terminal,variavel), ... ]
                | [ (terminal, variavel), 'ε'] <- Estado final
        '''
        self.productions = {}
        self.generate_grammar(automaton)

    def __str__(self):
        output = ''
        for variableIn in self.productions:
            derivations = self.productions[variableIn]
            derivations_str = map(str, derivations)
            joined = ' | '.join(derivations_str)
            output = '{}{} -> {},\n'.format(output, variableIn, joined)
        return output


    def generate_grammar(self, automaton: Automaton):
        variable_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        state_to_variable: Dict[str, str] = {}

        # Cria todas as listas de produções de cada variavel (vazias)
        for state in automaton.states:
            current = len(state_to_variable)
            if current < len(variable_names):
                variable = variable_names[current] 
            else:
                variable = state
            self.productions[variable] = []
            state_to_variable[state] = variable

        # Preenche as listas de produções
        for trans_input in automaton.prog_function:
            new_state = automaton.prog_function[trans_input]
            input_variable = state_to_variable[trans_input.state]
            output_variable = state_to_variable[new_state]
            # Produção do estado transition[0] recebe (transition[1], new_state)
            output = Derivation(
                    terminal=trans_input.symbol,
                    variable=output_variable)
            self.productions[input_variable].append(output)
        
        # Para as variaveis finais, gera uma transição para palavra vazia
        for state in automaton.finals:
            variable = state_to_variable[state]
            self.productions[variable].append(END_OUTPUT)
        
        # Define a variavel inicial
        self.initial = state_to_variable[automaton.initial]

    def derive(self, symbol: str, current_var: str) -> Optional[Derivation]:
        for derivation in self.productions[current_var]:
            if derivation.terminal == symbol:
                return derivation
        return None

    def verify_grammar(self, word):
        derivations = []

        # Sets iniciais
        current_var = self.initial  # seta o símbolo inicial

        # Leitura simbolo a simbolo da palavra
        for symbol in word:
            derivation = self.derive(symbol, current_var)
            if derivation is None:
                return None
            derivations.append(derivation)
            current_var = derivation.variable

        # Ultimo elemento sera dupla da palavra vazia (se existir)
        derivation = self.derive('', current_var)
        return None if derivation is None else derivations
