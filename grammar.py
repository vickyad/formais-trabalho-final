import string

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
            self.productions[state].append('ε')
        
        # Define a variavel inicial
        self.initial = initial


    def print_produtions(self):
        for var, transitions in self.productions.items():
            print(var, '->', transitions)