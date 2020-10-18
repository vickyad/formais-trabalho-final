'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte
    Alunos: Bruno Zimmermann, Jordi Pujol e Victoria Duarte
'''
from automaton import read_automaton
from grammar import Grammar
import sys
from os import path

# CONSTANTES
NOP = -1
EXIT = 0
PRINT_GRAMMAR = 1
EVAL_WORD = 2
EVAL_WORDS = 3


# Pede nome do arquivo que contém o autômato
file_name = input("Insira o nome do arquivo de automato >> ")
file_tuple = path.splitext(file_name)

# Adiciona extensão ao arquivo, caso esta não exista
if file_tuple[1] == '':
    file_name += '.txt'

''' item a '''
''' 
    Construa a gramática regular (GR) G equivalente a M 
'''
'''
    definition -> lista da definição parseada
    transition -> dicionario com transições
''' 
# Constroi a gramática
automaton = read_automaton(file_name)
grammar = Grammar(automaton)

# Inicializa variável
option = NOP

# Loop enquanto o usuário não escolher a opção de sair do programa
while option != EXIT:
    # Print do menu de opções
    print('\n')
    print("-" * 33)
    print("", PRINT_GRAMMAR, "-> Imprimir gramática")
    print("", EVAL_WORD, "-> Avaliar 1 (uma) palavra")
    print("", EVAL_WORDS, "-> Avaliar múltiplas palavras")
    print("", EXIT, "-> Encerrar programa")
    print("-" * 33)
    print("\nInforme a operação desejada:")
    option = int(input(">> "))

    # Opção de imprimir a gramática
    if option == PRINT_GRAMMAR:
        print(grammar)

    # Opção de avaliar uma palavra    
    elif option == EVAL_WORD:
        ''' item b '''
        ''' 
            Dada uma palavra w, indique se w pertence ou não a GERA(G), usando a GR construída no item 1.a. 
            Caso pertença, o programa deve apresentar a sequência de derivações que gera w em G.
        '''
        word = input("Digite uma palavra >> ").strip()
        derivation = grammar.derive(word)

        if derivation is None:
            print("Palavra não pertence à linguagem")
        else:
            print(derivation)
            
    # Opção de avaliar múltiplas palavras
    elif option == EVAL_WORDS:
        ''' item c '''
        '''
            Dada uma lista de palavras l, usando a GR construída no item 1.a, classificar cada palavra de l, 
            particionando a lista nos conjuntos ACEIT A = {w | w ∈ GERA(G)} e REJEIT A = {w | w 6∈ GERA(G)}, 
            e apresentar os dois conjuntos.
        '''
        aceita = []
        rejeita = []

        # Adiciona extensão ao arquivo, caso esta não exista
        file_name = input("Insira o nome do arquivo .CSV >> ")
        if file_tuple[1] == '':
            file_name += '.csv'

        # Avalia cada palavra e adiciona a lista de palavras aceitas ou rejeitadas
        with open(file_name, 'r') as file:
            for word in file:
                derivation = grammar.derive(word.strip())

                if derivation is None:
                    aceita.append(word.strip())
                else:
                    rejeita.append(word.strip())

        # Conjunto de palavras aceitas
        print("ACEITA:")
        for word in aceita:
            print(word)

        # Conjunto de palavras rejeitadas
        print("\nREJEITA:")
        for word in rejeita:
            print(word)

    # Opção de sair do programa
    elif option == EXIT:
        pass

    # Caso o input inserido não corresponda a uma opção existente
    else:
        print("Opção inválida, insira um número válido")

    # Espera enter para continuar o laço
    input("ENTER para continuar...")