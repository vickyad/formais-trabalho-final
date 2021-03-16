# INF05005 - Linguagens Formais E Autômatos N
### Semestre: 2020/1
#### Professor: Lucio Mauro Duarte

## Descrição
Criar um programa que, dado um autômato finito determinístico (AFD) M que a reconhece uma linguagem regular L, definido em um arquivo texto, execute as seguintes operações:
1. Construa a gramática regular (GR) G equivalente a M;
2. Dada uma palavra w, indique se w pertence ou não a GERA(G), usando a GR construída no item 1.a. Caso pertença, o programa deve apresentar a sequência de derivações que gera w em G;
3. Dada uma lista de palavras l, usando a GR construída no item 1.a, classificar cada palavra de l, particionando a lista nos conjuntos ACEIT A = {w | w ∈ GERA(G)} e REJEIT A = {w | w 6∈ GERA(G)}, e apresentar os dois conjuntos.

### Formato do arquivod de entrada
O formato do arquivo de entrada contendo a definição do AFD deve seguir o seguinte padrão:
```
<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},Prog,<ini>,{ <f0>,...,<fn>})
Prog
(<q0>,<s1>)=<q1>
...
(<qn>,<sn>)=<q0>

onde:
  < M >: nome dado ao autômato;
  < qi >: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado do autômato;
  < si >: para 1 ≤ i ≤ n, com n ∈ N e n ≥ 1, representa um símbolo do alfabeto da linguagem reconhecida pelo autômato;
  < ini >: indica o estado inicial do autômato, sendo que ini é um estado do autômato;
  < f i >: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado final do autômato, sendo que f i é um estado do autômato;
  (< qi >, < si >) =< qj >: descreve a função programa aplicada a um estado qi e um símbolo de entrada si que leva a computação a um estado qj.
```
### Exemplo:
AUTÔMATO=({q0,q1,q2,q3},{a,b},Prog,q0,{q1,q3})\
Prog\
(q0,a)=q1\
(q0,b)=q2\
(q1,b)=q2\
(q2,a)=q3\
(q2,a)=q2\
(q3,a)=q3\
(q3,b)=q2

