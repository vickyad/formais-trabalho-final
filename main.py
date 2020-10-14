'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte

    Alunos: Bruno Zimmermann, Jordi Pujol e Victoria Duarte
'''
from automaton_convert import read_automaton
from grammar import Grammar, derivations_to_str

''' EXERCICIO 1 '''
''' item a '''

'''
    definition -> lista da definição parseada
    transition -> dicionario com transições
''' 
automaton = read_automaton('testinho.txt')

grammar = Grammar(automaton)

print(grammar)

''' item b '''
# o programa vai receber um input de palavra, mas por agora vamos usar uma palavra fixa para testes
# word = input("digite uma palavra: ").strip()

word = 'abaaa'

derivations = grammar.verify_grammar(word)

print(derivations_to_str(derivations))
