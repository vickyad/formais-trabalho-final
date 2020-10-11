'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte

    Alunos: Bruno Zimmerman, Jordi Pujol e Victoria Duarte
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

grammar.print_produtions()