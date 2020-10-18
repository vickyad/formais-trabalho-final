'''
TRABALHO FINAL
LINGUAGENS FORMAIS E AUTOMATOS - 2020
Prof. Lucio Duarte

Alunos: Bruno Zimmermann, Jordi Pujol e Victoria Duarte
'''

import string

from typing import NamedTuple, Optional, List, Dict
from automaton import Automaton

class ProdOutput(NamedTuple):
    '''
    A saída de uma produção. Sempre no format aA. A exceção é a palavra vazia.

    O campo 'terminal' é o símbolo terminal da saída. Corresponde a "a" no
    formato acima. Vazio se a saída é a palavra vazia.

    O campo 'variable' é a variável da saída. Corresponde a "A" no formato
    acima. Vazio se a saída é a palavra vazia.
    '''
    
    terminal: str
    variable: str
    
    def __str__(self) -> str:
        '''
        Converte essa saída para representação textual.
        '''
        
        # Lida com a palavra vazia.
        if self.terminal == '' and self.variable == '':
            return 'ε'

        # Outros casos.
        return '{}{}'.format(self.terminal, self.variable)

# Saída final de uma produção.
EMPTY_OUTPUT: ProdOutput = ProdOutput(terminal='', variable='')

class Production(NamedTuple):
    '''
    Uma possível produção feita pela gramática. No format "A -> aB" ou "A -> ε".

    O campo 'input' corresponde à entrada da produção (no exemplo acima, "A").

    O campo 'output' corresponde à saída da produção (no exemplo acima, "aB" ou
    "ε").
    '''

    input: str
    output: ProdOutput

    def __str__(self) -> str:
        '''
        Representação textual da produção.
        '''
        return '{} -> {}'.format(self.input, self.output)

# Tipo das saídas das produções. Sempre na forma aA, ou ε na última transição.
class Derivation(NamedTuple):
    '''
    Uma derivação de uma palavra. A derivação é o caminho que a gramática faz
    para produzir uma palavra.

    O campo 'steps' representa os passos, em termos de produções, para chegar
    na palavra final.
    '''

    steps: List[Production]

    def __str__(self) -> str:
        '''
        Converte uma derivação em texto.
        '''

        # Na palavra em si ainda não tem nada.
        word = ''
        # Texto começa com o símbolo inicial.
        text = self.steps[0].input

        # Para todos os passos da derivação, faça:
        for step in self.steps:
            # Coloca o terminal na palavra.
            word = '{}{}'.format(word, step.output.terminal)
            # Adiciona o passo atual na saída junto com a palavra atual.
            text = '{} => {}{}'.format(text, word, step.output.variable)

        # Retornar a string construída.
        return text


class Grammar:
    '''
    Uma gramática regular à direita.

    O campo 'terminals' é uma lista de símbolos terminais, o alfabeto.

    O campo 'productions' é um dicionário que mapeia variáveis para possíveis
    saídas em tal que sejam parte de uma produção. Sempre no formato:
    "A -> aB", com exceção do caso "A -> ε".

    O campo 'initial' define a variável inicial da gramática.
    '''

    terminals: List[str]
    productions: Dict[str, List[ProdOutput]]
    initial: str

    def __init__(self, automaton: Automaton):
        '''
        Inicializa a gramática a partir de um autômato finit determinístico.
        '''

        # Inicializa produções como vazias.
        self.productions = {}

        # Os dois alfabetos são o mesmo.
        self.terminals = automaton.alphabet

        # Inicializa variáveis e retorna o mapeamento estado -> variável.
        state_to_variable = self.init_variables(automaton)
        # Inicializa o símbolo inicial para corresponder ao estado inicial.
        self.initial = state_to_variable[automaton.initial]
        # Gera as produções.
        self.make_productions(automaton, state_to_variable)
        # Marca os estados finais.
        self.mark_finals(automaton, state_to_variable)

    def init_variables(self, automaton: Automaton) -> Dict[str, str]:
        '''
        Inicializa as variáveis  da gramática a partir dos estados de um
        autômato. Returna o mapeamento de estados para variáveis.
        '''

        # Lista de letras disponíveis.
        variable_names = "ABCDEFGHIJKLMNOPQRTUVWXYZ"
        # Primeira letra disponível.
        cursor = 0
        # Iniciaiza o mapeamento, o dicionário.
        state_to_variable: Dict[str, str] = { }

        # Para cada estado do autômato, faça:
        for state in automaton.states:
            # Índice da primeira letra disponível.
            current = len(state_to_variable)

            # Esse estado é o inicial?
            if state == automaton.initial:
                # Se sim, vamos usar a convenção S.
                variable = 'S'
            # Existem letras disponíves?
            elif cursor < len(variable_names):
                # Se sim, use.
                variable = variable_names[cursor] 
                # A letra atual não está mais disponível.
                cursor += 1
            else:
                # Senão, paciência, vamos usar o nome do estado.
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
            state_to_variable: Dict[str, str]) -> None:
        '''
        Gera as produções da gramática a partir da função programa de um
        autômato e o mapeamento de estados pra variáveis.
        '''

        # Para cada transição:
        for trans_input, new_state in automaton.prog_function.items():
            # Variável correspondenete ao estado de entrada.
            input_variable = state_to_variable[trans_input.state]
            # Variável correspondenete ao estado de saída.
            output_variable = state_to_variable[new_state]
            # Instancia a saída da produção.
            output = ProdOutput(
                    terminal=trans_input.symbol,
                    variable=output_variable)
            # Adiciona a saída à lista de saídas possíveis daquela variável.
            self.productions[input_variable].append(output)

    def mark_finals(
            self,
            automaton: Automaton,
            state_to_variable: Dict[str, str]) -> None:
        '''
        Marca as variáveis da gramática como "finais" quando correspondem a
        algum estado final de um autômato. Marcar como final significa fazer
        com que a variável possa ser substituída pela palavra vazia.
        '''

        # Para cada estado final.
        for state in automaton.finals:
            variable = state_to_variable[state]
            # Adicione a saída de produção que resulta na palavra vazia dada
            # a variável de entrada.
            self.productions[variable].append(EMPTY_OUTPUT)

    def __str__(self) -> str:
        '''
        Converte a gramática para texto. Método mágico do Python.
        '''
        
        # Colocando variáveis e terminains em duas string, com os elementos 
        # separados por vírgulas.
        variables = ','.join(self.productions.keys())
        terminals = ','.join(self.terminals)

        # Começamos com o cabeçalho da definição.
        definition = 'GRAMMAR=({{{}}},{{{}}},Prod,{})\nProd\n'
        text = definition.format(variables, terminals, self.initial)

        # Para cada variável de entrada de uma produção, e lista de saídas de
        # uma produção para aquela variável, faça:
        for inputVariable, outputs in self.productions.items():
            # Só usar essa variável se tiver uma produção.
            if len(outputs) > 0:
                # Converte cada saída para string.
                outputs_str = map(str, outputs)
                # Junta todas saídas usando ' | '.
                joined = ' | '.join(outputs_str)
                # Coloca as produções daquela variável em uma linha.
                text = '{}{} -> {}\n'.format(text, inputVariable, joined)

        # Retorna a string produzida.
        return text 

    def find_production(
            self,
            current_variable: str,
            symbol: Optional[str]) -> Optional[Production]:
        '''
        Encontra uma produção que contenha o dado símbolo 'symbol', e que
        substitua a dada variável 'current_variable'.

        Caso a produção seja encontrada, ela é retornada. Caso não seja
        encontrada uma produção, None é retornado.
        '''

        # Para cada saída de uma produção com a dada variável de entrada:
        for output in self.productions[current_variable]:
            # Se o terminal desta saída for o nosso símbolo, encontramos.
            if output.terminal == symbol:
                return Production(input=current_variable, output=output)
        # Não há produção para a variável atual e o símbolo necessário.
        return None

    def derive(self, word: str) -> Optional[Derivation]:
        '''
        Verifica se uma palavra segue a gramática, e, portanto, se a palavra
        é parte da linguagem gerada pela gramática.
        '''

        # Inicializa a lista de passos da derivação como contendo somente o
        # primeiro passo.
        productions = []

        # A primeira variável é o símbolo inicial.
        current_variable = self.initial

        for symbol in word:
            # Tenta encontrar uma produção.
            production = self.find_production(current_variable, symbol)
            if production is None:
                # Se não achou, a palavra não faz parte da linguagem.
                return None
            # Adiciona a produção encontrada à lista de passos.
            productions.append(production)
            # Nova variável vem da saída da produção.
            current_variable = production.output.variable

        # Por último, precisamos encontrar uma produção para a variável final
        # que resulte na palavra vazia.
        production = self.find_production(current_variable, '')
        # Se não achar, a linguagem não contém a palavra.
        if production is None:
            return None

        # Se achou, tudo certo, retorne a derivação.
        productions.append(production)
        return Derivation(steps=productions)
