import string

from typing import NamedTuple, Optional, List, Dict
from automaton import Automaton

# Tipo das saídas das produções. Sempre na forma aA, ou ε na última transição.
class Derivation(NamedTuple):
    '''
    Uma derivação de uma gramática regular à direita. Saída de uma produção.
    Sempre no formato "aA", onde "a" é um terminal, e "A" é uma variável. A
    exceção é o caso da derivação que no formato "ε" (palavra vazia).

    O campo 'terminal' é o símbolo terminal dessa derivação, com exceção do caso
    da palavra vazia.

    O campo 'variable' é a variável dessa derivação, que só existe se o terminal
    não for a palavra vazia, ou seja, é None se terminal for a palavra vazia.
    '''

    terminal: str
    variable: Optional[str]

    # Representação textual.
    def __str__(self):
        '''
        Converte esta derivação para texto. Método mágico do Python.
        '''

        # Testa se essa derivação resulta na palavra vazia.
        if self.variable is None:
            # Se sim, retorna o símbolo para a palavra vazia.
            return 'ε'
        # Senão, retorna o terminal seguido da variável.
        return '{}{}'.format(self.terminal, self.variable)

# Saída final de uma produção.
EMPTY_DERIVATION: Derivation = Derivation(terminal='', variable=None)

def derivations_to_str(derivations: List[Derivation]) -> str:
    '''
    Converte uma lista de derivações em texto.
    '''

    # A palavra começa vazia.
    word = ''
    # Começamos sem nada na string de saída.
    output = ''

    # Para todas as derivações, faça:
    for derivation in derivations:
        # Coloca o terminal na palavra.
        word = '{}{}'.format(word, derivation.terminal)
        # Adiciona a derivação atual na saída junto com a palavra atual.
        output = '{}{}{} => '.format(output, word, derivation.variable)

    # Adicionar o passo onde se substitui a última variável pela palavra vazia.
    output = '{}{}'.format(output, word)
    # Retornar a output construída.
    return output

class Grammar:
    '''
    Uma gramática regular à direita.

    O campo 'productions' é um dicionário que mapeia variáveis para possíveis
    derivações. Sempre no formato: "A -> aB", com exceção do caso "A -> ε".

    O campo 'initial' define a variável inicial da gramática.
    '''

    productions: Dict[str, List[Derivation]]
    initial: str

    def __init__(self, automaton: Automaton):
        '''
        Inicializa a gramática a partir de um autômato finit determinístico.
        '''

        # Inicializa produções como vazias.
        self.productions = {}

        # Inicializa variáveis e retorna o mapeamento estado -> variável.
        state_to_variable = self.init_variables(automaton)
        # Gera as produções.
        self.make_productions(automaton, state_to_variable)
        # Inicializa o símbolo inicial para corresponder ao estado inicial.
        self.initial = state_to_variable[automaton.initial]
        # Marca os estados finais.
        self.mark_finals(automaton, state_to_variable)

    def init_variables(self, automaton: Automaton) -> Dict[str, str]:
        '''
        Inicializa as variáveis  da gramática a partir dos estados de um
        autômato. Returna o mapeamento de estados para variáveis.
        '''

        # Lista de letras disponíveis.
        variable_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Iniciaiza o mapeamento, o dicionário.
        state_to_variable = {}

        # Para cada estado do autômato, faça:
        for state in automaton.states:
            # Índice da primeira letra disponível.
            current = len(state_to_variable)
            # Existem letras disponíves?
            if current < len(variable_names):
                # Se sim, use.
                variable = variable_names[current] 
            else:
                # Se não, paciência, vamos usar o nome do estado.
                variable = state
            # As produções para esta variável começam vazias.
            self.productions[variable] = []
            # Mapeia o estado para a variável.
            state_to_variable[state] = variable

        # Retorna o mapeamento estado -> variável.
        return state_to_variable

    def make_productions(
            self,
            automaton: Automaton,
            state_to_variable: Dict[str, str]):
        '''
        Gera as produções da gramática a partir da função programa de um
        autômato e o mapeamento de estados pra variáveis.
        '''

        # Para cada transição:
        for trans_input in automaton.prog_function:
            # Estado de saída.
            new_state = automaton.prog_function[trans_input]
            # Variável correspondenete ao estado de entrada.
            input_variable = state_to_variable[trans_input.state]
            # Variável correspondenete ao estado de saída.
            output_variable = state_to_variable[new_state]
            # Instancia a derivação.
            derivation = Derivation(
                    terminal=trans_input.symbol,
                    variable=output_variable)
            # Adiciona a derivação à lista de derivações possíveis daquela
            # variável.
            self.productions[input_variable].append(derivation)

    def mark_finals(
            self,
            automaton: Automaton,
            state_to_variable: Dict[str, str]):
        '''
        Marca as variáveis da gramática como "finais" quando correspondem a
        algum estado final de um autômato. Marcar como final significa fazer
        com que a variável possa ser substituída pela palavra vazia.
        '''

        # Para cada estado final.
        for state in automaton.finals:
            variable = state_to_variable[state]
            # Adicione a derivação que resulta na palavra vazia para as
            # produções da variável correspondente.
            self.productions[variable].append(EMPTY_DERIVATION)


    def __str__(self):
        '''
        Converte a gramática para texto. Método mágico do Python.
        '''
        
        # Começamos com a string de saída vazia.
        output = ''
        # Para cada variável.
        for variableIn in self.productions:
            # Pegando as produções cuja entrada seja a variável.
            derivations = self.productions[variableIn]
            # Só usar essa variável se tiver uma produção.
            if len(derivations) > 0:
                # Converte cada derivação para string.
                derivations_str = map(str, derivations)
                # Junta todas derivações usando ' | '.
                joined = ' | '.join(derivations_str)
                # Coloca as produções daquela variável em uma linha.
                output = '{}{} -> {},\n'.format(output, variableIn, joined)
        # Retorna a string produzida.
        return output

    def derive(self, symbol: str, current_var: str) -> Optional[Derivation]:
        '''
        Encontra uma derivação que contenha o dado símbolo 'symbol', e que
        substitua a dada variável 'current_var'.

        Caso a derivação seja encontrada, ela é retornada. Caso não seja
        encontrada uma derivação, None é retornado.
        '''

        # Para cada produção:
        for derivation in self.productions[current_var]:
            # Se o terminal desta derivação for o nosso símbolo, encontramos.
            if derivation.terminal == symbol:
                return derivation
        # Não há derivação para a variável atual e o símbolo necessário.
        return None

    def derive_word(self, word):
        '''
        Verifica se uma palavra segue a gramática, e, portanto, se a palavra
        é parte da linguagem gerada pela gramática.
        '''

        # Inicializa as derivações como sem derivações no momento.
        derivations = []

        # A primeira variável é o símbolo inicial.
        current_var = self.initial

        # Leitura simbolo a simbolo da palavra
        for symbol in word:
            # Tenta encontrar uma derivação.
            derivation = self.derive(symbol, current_var)
            if derivation is None:
                # Se não achou, a palavra não faz parte da linguagem.
                return None
            # Adiciona a derivação encontrada à lista de derivações.
            derivations.append(derivation)
            # Nova variável vem da derivação.
            current_var = derivation.variable

        # Por último, precisamos encontrar uma derivação para a variável final
        # que seja a palavra vazia.
        derivation = self.derive('', current_var)
        # Se não achar, a linguagem não contém a palavra.
        if derivation is None:
            return None
        # Se achou, tudo certo, retorne as derivações.
        return derivations
