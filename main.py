'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte

    Alunos: Bruno Zimmermann, Jordi Pujol e Victoria Duarte
'''
from automaton_convert import *
from grammar import *

''' EXERCICIO 1 '''
''' item a '''

'''
    definition -> lista da definição parseada
    transition -> dicionario com transições
''' 
definition, transitions = read_automaton('testinho.txt')

grammar = Grammar(definition, transitions)


# grammar.print_produtions()

''' item b '''
# o programa vai receber um input de palavra, mas por agora vamos usar uma palavra fixa para testes
# word = input("digite uma palavra: ").strip()

word = 'abaaa'

retorno = grammar.verify_grammar(word)

print(retorno)