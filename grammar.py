import string


# Indices para recuperar valores nas duplas
TERMINAL = 0
VARIAVEL = 1

# Palavra vazia
VAZIA    = 'ε'


class Grammar:
    def __init__(self, definition, transitions):
        '''
            Dicionario de listas duplas, onde cada valor:
            variavel : lista_produções
            lista_produções : 
                | [ (terminal, variavel), (terminal,variavel), ... ]
                | [ (terminal, variavel), 'ε'] <- Estado final
        '''
        self.productions = {}
        ''' Estado inicial '''
        self.initial = ''
        self.generate_grammar(definition, transitions)


    def generate_grammar(self, definition, transitions):
        states = definition[0]
        initial = definition[2]
        finals = definition[3]

        # Cria todas as listas de produções de cada variavel (vazias)
        for state in states:
            self.productions[state] = []
        
        # Preenche as listas de produções
        for transition, new_state in transitions.items():
            # Produção do estado transition[0] recebe (transition[1], new_state)
            self.productions[transition[0]].append( (transition[1], new_state) )
        
        # Para as variaveis finais, gera uma transição para palavra vazia
        for state in finals:
            self.productions[state].append(tuple(VAZIA))
        
        # Define a variavel inicial
        self.initial = initial


    def print_produtions(self):
        for var, productions in self.productions.items():
            print(var, '->', productions)


    def verify_grammar(self, word):
        print(f'to tentando avaliar a palavra {word}')

        word_m = word + VAZIA     # Acrescenta o símbolo de palavra vazia ao final da palavra,
                                # para que a gramática possa identificar parada por aceitação

        returned_list = []

        # Sets iniciais
        current_state = self.initial  # seta o estado inicial
        productions = f'S -> {current_state}\n'   # inicia as transições realizadas na verificação
        interrupted = False     # flag que indica se a palavra foi aceita ou não (se houve interrupção do laço for
                                # mais externo a plavra foi rejeitada. Caso contrário, foi aceita)

        # Leitura simbolo a simbolo da palavra
        for symbol in word_m:
            # Verifica se a palavra terminou em um estado final
            # Sendo aprovada, termina o loop
            if symbol == VAZIA:
                # Ultimo elemento sera dupla da palavra vazia (se existir)
                if self.productions[current_state][-1][TERMINAL] == VAZIA:
                    #Retorno da palavra aceita e manda msg fofa
                    print("achei :3")
                    return returned_list
                else:
                    #Retorna None e xinga o usuário
                    print("PALAVRA NÃO ACEITA, OTÁRIO")
                    return None

            # Procura o simbolo na lista de produções
            found = False
            for element in self.productions[current_state]:
                # Se encontrado, adiciona o par na lista para retorno e seta flag p/ True
                if element[TERMINAL] == symbol:
                    returned_list.append((current_state, element))
                    current_state = element[VARIAVEL]
                    found = True
            
            # Se não for encontrada transições, xinga o usuário e retorna None
            if not found:
                print("PALAVRA ERRADA, SEU LIXO")
                return None