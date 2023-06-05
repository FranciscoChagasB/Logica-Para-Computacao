from z3 import *

def create_schedule_formula(courses, num_slots, pairs):
    #Criando variáveis
    variables = [[Bool(f'x{c}_{s}') for s in range(num_slots)] for c in courses]

    #Instanciando solver
    solver = Solver()

    #1. Cada minicurso deve ser ofertado em pelo menos um slot.
    for c in courses:
        clause = Or([variables[c-1][s] for s in range(num_slots)])
        solver.add(clause)

    #2.Cada minicurso deve ser ofertado em no máximo um slot.
    for c1 in courses:
        for s1 in range(num_slots):
            for s2 in range(s1 + 1, num_slots):
                clause = Or(Not(variables[c1-1][s1]), Not(variables[c1-1][s2]))
                solver.add(clause)

    #3. Minicursos com inscrições em comum não podem ser ofertados no mesmo slot.
    for (c1, c2) in pairs:
        for s in range(num_slots):
            clause = Or(Not(variables[c1-1][s]), Not(variables[c2-1][s]))
            solver.add(clause)

    return solver, variables

def solve_schedule(solver):
    #Solucionando o problema
    if solver.check() == sat:
        model = solver.model()
        return model

    return None

def extract_schedule(model, variables, course_names):
    #Extraindo dados
    schedule = {}

    for c, slots in enumerate(variables):
        for s, variable in enumerate(slots):
            if is_true(model[variables[c][s]]):
                schedule[course_names[c]] = f's{s+1}'
                break

    return schedule

#Entradas de exemplo
course_names = ['Java', 'Sql', 'Python', 'C#']
num_slots = 3
pairs = [(1, 2), (2, 3), (2, 4), (3, 4), (1, 3)]

#Criando as fórmulas
solver, variables = create_schedule_formula(range(1, len(course_names) + 1), num_slots, pairs)

#Solucionando o exemplo
model = solve_schedule(solver)

if model is not None:
    schedule = extract_schedule(model, variables, course_names)

    print("It is possible to schedule the courses.")
    print("Course schedule:")
    for course, slot in schedule.items():
        print(f"Course {course}: Slot {slot}")
else:
    print("It is not possible to schedule all the courses with the given slots.")
