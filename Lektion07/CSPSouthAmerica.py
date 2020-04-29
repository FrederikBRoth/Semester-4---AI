from random import shuffle


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result != "failure":
                    return result
                assignment.pop(var)
        return "failure"

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_south_america_csp():
    gyfr, su, gy, ve, co, pa, cos, ec, pe, ch, ar, ur, par, bo, br = 'Guyane (FR)', 'Suriname', \
                                                                     'Guyana', 'Venezuela', 'Colombia', 'Panama', \
                                                                     'Costa Rica', 'Ecuador', \
                                                                     'Peru', 'Chile', 'Argentina', \
                                                                     'Uruguay', 'Paraguay', 'Bolivia', 'Brasil'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [gyfr, su, gy, ve, co, pa, cos, ec, pe, ch, ar, ur, par, bo, br]
    domains = {
        gyfr: values[:],
        su: values[:],
        gy: values[:],
        ve: values[:],
        co: values[:],
        pa: values[:],
        cos: values[:],
        ec: values[:],
        pe: values[:],
        ch: values[:],
        ar: values[:],
        ur: values[:],
        par: values[:],
        bo: values[:],
        br: values[:]
    }
    neighbours = {
        gyfr: [gy, su],
        su: [gyfr, gy, br],
        gy: [su, ve, br],
        ve: [gy, co, br],
        co: [pa, ve, pe, br, ec],
        pa: [cos, co],
        cos: [pa],
        ec: [co, pe],
        pe: [co, bo, ch, br],
        ch: [pe, bo, ar],
        ar: [ch, bo, par, ur, br],
        ur: [ar, br],
        par: [ar, bo, br],
        bo: [pe, ch, ar, par, br],
        br: [gyfr, su, gy, ve, co, pe, bo, par, ar, ur]
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        gyfr: constraint_function,
        su: constraint_function,
        gy: constraint_function,
        co: constraint_function,
        pa: constraint_function,
        cos: constraint_function,
        ec: constraint_function,
        pe: constraint_function,
        ch: constraint_function,
        ar: constraint_function,
        ur: constraint_function,
        par: constraint_function,
        bo: constraint_function,
        br: constraint_function
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_south_america_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
