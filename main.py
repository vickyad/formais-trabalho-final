'''
    TRABALHO FINAL
    LINGUAGENS FORMAIS E AUTOMATOS - 2020
    Prof. Lucio Duarte

    Alunos: Bruno Zimmermann, Jordi Pujol e Victoria Duarte
'''
from automaton import read_automaton
from grammar import Grammar, derivations_to_str
import sys

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
# o programa vai receber um input de palavra, mas por agora vamos usar uma
# palavra fixa para testes
#
# word = input("digite uma palavra: ").strip()

# Pega argumento da linha de comando se tem. Se não tem, usa uma palavra fixa.
#
# Por exemplo:
#
# python main.py abaaa
if len(sys.argv) >= 2:
    word = ' '.join(sys.argv[1:])
else:
    word = 'abaaa'

derivations = grammar.derive_word(word)

if derivations is None:
    print("'", word, "' não faz parte da linguagem", sep='')
else:
    print(derivations_to_str(derivations))

