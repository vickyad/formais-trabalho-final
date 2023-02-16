# Regular Grammar and word reconigzer
### Course: Linguagens Formais e Autômatos N
#### Professor: Lucio Duarte
#### Semester: 2020/1
---

### Table of Contents

##### 1. [About this project](#about)

##### 2. [Technologies used](#stack)

##### 3. [Install and run the project](#installation)

##### 4. [How this project is organized](#organization)

##### 5. [Learn More](#learn-more)

---

<a name="about"></a>

## About this project

Given and Finite Automata M that recognizes the Regular Language L, defined in a text file, the program should execute the following tasks:

1. Construct a Regular Grammar G equivalent to M
2. Given a word w, define if w ∈ GERA(G), using the grammar G built in 1. If the word belongs to the grammar, execute all derivations that generate w
3. Given a list of words l, using the grammar G from item 1, classify each word from l in one of the sets: ACEITA = { w | w ∈ GERA(G) } or REJEITA = { w | w ∉ GERA(G) } 

### Entry file format
```
<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},Prog,<ini>,{ <f0>,...,<fn>})
Prog
(<q0>,<s1>)=<q1>
...
(<qn>,<sn>)=<q0>
```

where:
  < M >: automata name;
  < qi >: for 0 ≤ i ≤ n, with n ∈ N and n ≥ 0, represents an automata state;
  < si >: for 1 ≤ i ≤ n, with n ∈ N and n ≥ 1, represents a symbol of the alphabet of the recognized language;
  < ini >: indicate the initial state of the automata, with ini been an automata state;
  < fi >: for 0 ≤ i ≤ n, with n ∈ N and n ≥ 0, represents a final state of the automata, with si been an automata state;
  (< qi >, < si >) =< qj >: describes the function applied to an estate qi and a symbol si that computes to state qj.


### Example:
AUTÔMATO=({q0,q1,q2,q3},{a,b},Prog,q0,{q1,q3})\
Prog\
(q0,a)=q1\
(q0,b)=q2\
(q1,b)=q2\
(q2,a)=q3\
(q2,a)=q2\
(q3,a)=q3\
(q3,b)=q2

---

<a name="stack"></a>

## Technologies used

![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)

---

<a name="installation"></a>

## Install and run the project

After cloning the project, run the command:

```bash
python main.py
```

---

<a name="organization"></a>

## How this project is organized

This projects has a pretty basic folder structure

```bash
automaton.py
grammar.py
main.py
```

### `automaton.py`

Contains all the tools necessary to create a Finite Automata.

### `grammar.py`

Contains all the functions to handle the creation of Regular Grammar and the word verifications.

### `main.py`

Main file with the user interation loop.

---

<a name="learn-more"></a>

## Learn more

### Python

To learn more about Python, take a look at their documentation:

- [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)
