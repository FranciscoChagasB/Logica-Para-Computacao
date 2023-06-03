#Projeto ded lógica para computação usando o Sat Solver Z3.

from z3 import *

def cria_horario_curso(curso, n_slots, restricoes):
    #Criando variáveis
    variables = [[Bool(f'x{c}_{s}') for s in range(n_slots)] for c in curso] #Bool: tipo de dado para representar as variáveis booleanas 

    #Criando o solver 
    solver = Solver() #Instância da classe Solver() para adicionar as cláusulas da nossa fórmula e verificar sua satisfatibilidade.

    #1. Cada minicurso deve ser ofertado em pelo menos um slot.
    for c in curso:
        clause = Or([variables[c-1][s] for s in range(n_slots)]) #Or: função do conectivo lógico 'ou'.
        solver.add(clause)

    #2.Cada minicurso deve ser ofertado em no máximo um slot.
    for c1 in curso:
        for s1 in range(n_slots):
            for s2 in range(s1 + 1, n_slots):
                clause = Or(Not(variables[c1-1][s1]), Not(variables[c1-1][s2])) #Not: função do conectivo 'não'
                solver.add(clause)

    #3. Minicursos com inscrições em comum não podem ser ofertados no mesmo slot.
    for (c1, c2) in restricoes:
        for s in range(n_slots):
            clause = Or(Not(variables[c1-1][s]), Not(variables[c2-1][s]))
            solver.add(clause)

    return solver, variables
