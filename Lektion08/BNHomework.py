import functools
import random
from pprint import pformat


def multiply_vector_elements(vector):
    """ return the multiplication of the vector elements """

    def mult(x, y):
        return x*y

    return functools.reduce(mult, vector, 1)


class Variable(object):
    """ Node in the network. Represent a random Variable """

    def __init__(self, name, assignments, probability_table, parents=[], children=[]):
        """ Node initialization
            params:
            name: name of this random variable.
            assignments: possible values this variable can have.
            probability_table: the casual probability table of this variable.
            parents: list of references to this Node`s parents.
            children: list of references to this Node`s children.
        """

        # the name of this random variable
        self.name = name

        # holds the possible assignments of this random variable
        # assume certain order
        self.assignments = {}
        for i in range(len(assignments)):
            self.assignments[assignments[i]] = i

        # holds the distribution table of this random variable
        for key, val in probability_table.items():
            if val is  tuple:
                if len(val) != len(assignments):
                    self = None
                    raise ValueError(
                        'data in probability table is inconsistent with possible assignments')

        self.probability_table = probability_table

        # list of dependent variables
        self.children = children

        # list of variables which this variable depends upon
        self.parents = parents

        # holds the marginal, pre-calculated probability to obtain each
        # possible value
        self.marginal_probabilities = len(assignments) * [0]

        # indicates whether this node is ready to use
        # true when the marginal probabilities were calculated
        self.ready = False

    def get_name(self):
        """ return the name of this random variable """
        return self.name

    def get_assignments(self):
        """ return the possible values this variable can have """
        return self.assignments

    def get_assignment_index(self, assignment):
        """ returns the index of a given possible assignment within the assignments list """
        return self.assignments[assignment]

    def get_probability(self, value, parents_values):
        """ read from the distribution table and return the probability of having a
            certain value (value) given the values of the parents.
        """
        return self.probability_table[parents_values][self.assignments[value]]

    def get_conditional_probability(self, value, parents_values):
        """ read from the distribution table and return the probability of having a
            certain value (value) given the values of the parents.
            here the parents assignments can be partial
            parent_vals is a dictionary: { parent: value }
        """
        res = 0
        given_parents_index = []
        marginal_parents_index = []
        for i, v in enumerate(self.parents):
            if v.name in parents_values:
                given_parents_index.append((i, parents_values[v.name]))
            else:
                marginal_parents_index.append(i)

        # go over the rows in the distribution table
        for row_key, row_val in self.probability_table.items():
            valid_row = 1

            # check if this row should count for the marginal conditional
            # probability
            for gpi in given_parents_index:
                if row_key[gpi[0]] != gpi[1]:
                    valid_row = 0
                    break

            # if this row is valid, add the corresponding conditional
            # probability
            if valid_row:
                parents_probability = 1
                for mpi in marginal_parents_index:
                    parents_probability *= self.parents[mpi].get_marginal_probability(row_key[mpi])

                res += row_val[self.assignments[value]] * parents_probability
        return res

    def calculate_marginal_probability(self):
        """ calculates and stores the marginal probabilities of this node.
            this function should be call before any other calculation is done.
        """

        # return, if already done
        if self.ready:
            return

        marginals = list()
        true = 0
        false = 0

        for x in self.probability_table:
            if self.probability_table[x][1] is not 0:
                print(self.probability_table)
                false += self.probability_table[x][0]
                true += self.probability_table[x][1]
            else:
                true += self.probability_table[x][0]
        marginals.append(true)
        marginals.append(false)

        # COMPLETE THIS FUNCTION
        self.marginal_probabilities = marginals

        # set this Node`s state to ready
        self.ready = True

    def get_marginal_probability(self, val):
        """ returns the marginal probability, to have a certain value """
        return self.marginal_probabilities[self.assignments[val]]

    def add_child(self, node):
        """ add dependent Variable to this variable """
        self.children.append(node)

    def add_parent(self, node):
        """ add a parent to this Variable """
        self.parents.append(node)

    def get_children(self):
        """ returns the children list """
        return self.children

    def is_child_of(self, node):
        """ return boolean, indicating whether this Node is a child of a given
            Node
        """
        for var in self.parents:
            if var.name == node.name:
                return 1
        return 0


class BayesianNetwork(object):
    """ Bayesian Network implementation. This implementation incorporates few
        assumptions (see comments).
    """

    def __init__(self):
        """ Initialize connectivity matrix. """
        self.variables = []     # list of variables (Nodes)
        self.varsMap = {}       # a mapping of variable name to the actual node, for easy access
        self.ready = False          # indication of this net state

    def calculate_marginal_probabilities(self):
        """ pre-calculate and stores the marginal probabilities of all the nodes """

        # iterate over the Nodes, from parents to children
        for var in self.variables:
            var.calculate_marginal_probability()
        self.ready = True

    def get_variables(self):
        """ returns the variables """

        return self.variables

    def get_variable(self, varName):
        """ returns the variable with the given name """

        return self.varsMap[varName]

    def add_variable(self, var, index=-1):  # len(variables)):
        """ add a single Node to the net """

        if index < 0:
            self.variables.append(var)
        else:
            self.variables.insert(index, var)

        self.varsMap[var.name] = var
        self.ready = False  # we need to re-calculate marginals

    def set_variables(self, varList):
        """ quick assignment: set the given Node list to be the Nodes of this
            net
        """

        self.variables = varList
        for var in self.variables:
            self.varsMap[var.name] = var
        self.ready = False  # we need to re-calculate marginals

    def get_marginal_probability(self, var, val):
        """ returns the marginal probability of a given node """

        return var.get_marginal_probability(val)

    # values is dictionary
    def get_joint_probability(self, values):
        """ return the joint probability of the Nodes """

        joinprob = 0
        problist = list()
        # COMPLETE THIS FUNCTION
        for var in self.variables:
            name = var.name
            for value in values:
                valueName = ""
                if value == name:
                    valueName = name
            if len(var.parents) is not 0:
                probabilities = var.probability_table
                stateTuple = tuple()
                parentStates = list()
                for parent in var.parents:
                    parentStates.append(values[parent.name])
                stateTuple = tuple(parentStates)

                state = var.probability_table[stateTuple]

                if(values[name] == "false"):
                    problist.append(state[1])
                else:
                    problist.append(state[0])
            else:
                for x in var.probability_table:
                    if (values[name] == "false"):
                        problist.append(var.probability_table[x][1])
                    else:
                        problist.append(var.probability_table[x][0])
        print(problist)
        for x in problist:
            if problist.index(x) == 0:
                joinprob = x
            else:
                joinprob *= x
        return joinprob

    def get_conditional_probability(self, values, evidents):
        """ returns the conditional probability.
            Here I do not introduce advanced algorithms for inference (e.g. junctions trees)
            this method implement only simple inference, namely: the joint probability of children given their parents
            or the probability of parents given their children.
            assumption: variables in each level are independent, or independent given their parents
            (i.e vars in values are independent, as well as vars in evidents
        """
        res = 1

        # when we want probability of children given their parents
        # if self.varsMap[list(values.keys())[0]].is_child_of(self.varsMap[list(evidents.keys())[0]]):
        if all(self.varsMap[list(values.keys())[0]].is_child_of(self.varsMap[evident]) for evident in evidents.keys()):
            # print('probability of children given their parents')
            for child, c_val in values.items():
                res *= self.varsMap[child].get_conditional_probability(c_val, evidents)

        # when we want probability of parents given their children
        # make use of Bayes rule
        # assumption: nodes in each level are independent, given their parents
        else:
            print('probability of parents given their children')

            joint_marginal_parents = 1
            joint_marginal_children = 1
            joint_conditional_children = 1
            marginal_of_evidents = 1

            # calculating the joint probability of the parents
            for parent, p_val in values.items():
                joint_marginal_parents *= self.varsMap[parent].get_marginal_probability(p_val)

            # calculating the joint probability of the children, and the joint joint probability
            # of the children given their parents
            for child, c_val in evidents.items():
                joint_marginal_children *= self.varsMap[child].get_marginal_probability(c_val)

                # children given their parents. here the values become the
                # evidents!
                joint_conditional_children *= self.varsMap[child].get_conditional_probability(c_val, values)

                k = list(values.keys())[0]
                complementary_conditional_values = values.copy()
                complementary_conditional_values[k] = 'false' if values[k] == 'true' else 'true'
                marginal_of_evidents = marginal_of_evidents * self.varsMap[child].get_conditional_probability(c_val, complementary_conditional_values)

                # print("Child: {}".format(child))
                # print("    Given: {}".format(complementary_conditional_values))

            # uses Bayes rule, for calculating the conditional probability
            res = (joint_conditional_children * joint_marginal_parents) / ((joint_conditional_children * joint_marginal_parents) + marginal_of_evidents * (1 - joint_marginal_parents))

        return res

    # helper method
    def sub_vals(self, var, values):
        """ return a tuple, contain all the relevant
            assignments for the given variable (i.e - the assignments
            pertaining to the variable`s parents."""
        sub = []
        for p in var.parents:
            sub.append(values[p.name])
        return tuple(sub)


def create_random_sample(network):
    """ creates random sample for the given network.
        the distribution of the samples follows the joint probability function.
        assumes binary variables. """
    sample = {}
    for var in network.variables:

        samp = random.random()
        assignment1 = list(var.assignments.keys())[0]
        assignment2 = list(var.assignments.keys())[0]

        parents_values = network.sub_vals(var, sample)
        prob = var.get_probability(assignment1, parents_values)

        if samp <= prob:
            sample[var.name] = assignment1
        else:
            sample[var.name] = assignment2
    return sample


def pad(string, pad=4):
    lines = string.split('\n')
    padded_lines = (' ' * pad + line for line in lines)
    return '\n'.join(padded_lines)


def print_conditional_probability(network, conditionals_vars, conditionals_evidents):
    print('Given')
    print(pad(pformat(conditionals_evidents)))
    print('conditional probability of')
    print(pad(pformat(conditionals_vars)))
    print("is {:f}".format(
        network.get_conditional_probability(
            conditionals_vars,
            conditionals_evidents
        )))


def print_joint_probability(network, values):
    print('Joint probability of')
    print(pad(pformat(values)))
    print("is {:f}".format(network.get_joint_probability(values)))


def print_marginal_probabilities(network):
    print("Marginal probabilities:")
    for variable in network.get_variables():
        print("    {}".format(variable.get_name()))
        for assignment in variable.get_assignments():
            print("        {}: {:f}".format(
                assignment,
                variable.get_marginal_probability(assignment))
            )


def sprinkler():
    # the values kept as dictionary
    t1 = {(): (0.3, 0.7)}
    t2 = {(): (0.2, 0.8)}
    t3 = {(): (0.3, 0.7)}
    #It looks like that to be able to create the probabilities as tuples. Not optimal but it works
    t4 = {
        ('true', 'true'): (0.05, 0),
        ('true', 'false'): (0.6, 0),
        ('false', 'true'): (0.3, 0),
        ('false', 'false'): (0.7, 0)
    }
    t5 = {
        ('true', 'true', 'true'): (0.9, 0),
        ('true', 'true', 'false'): (0.8, 0),
        ('true', 'false', 'true'): (0.3, 0),
        ('true', 'false', 'false'): (0.2, 0),
        ('false', 'true', 'true'): (0.6, 0),
        ('false', 'true',  'false'): (0.5, 0),
        ('false', 'false', 'true'): (0.1, 0),
        ('false', 'false', 'false'): (0.01, 0)
    }
    t6 = {('true',): (0.7,0), ('false',): (0.1,0)}

    # creation of Nodes objects
    dt = Variable('Damaged Tire', ('true', 'false'), t1)
    ftl = Variable('Fuel Tank Leaking', ('true', 'false'), t2)
    em = Variable('Electronics Malfunctioning', ('true', 'false'), t3)
    sms = Variable('Slow Max Speed', ('true',), t4, [dt, em])
    hc = Variable('High Consumption', ('true',), t5, [dt, em, ftl])
    v = Variable('Vibrations', ('true',), t6, [dt])

    variables = [dt, ftl, em, sms, hc, v]

    # creation of Network
    network = BayesianNetwork()
    network.set_variables(variables)

    # pre-calculate marginals
    network.calculate_marginal_probabilities()

    print_marginal_probabilities(network)

    print('')

    joint_values = {
        'Damaged Tire': 'true',
        'Fuel Tank Leaking': 'false',
        'Electronics Malfunctioning': 'false',
        'Slow Max Speed': 'true',
        'High Consumption': 'true',
        'Vibrations': 'true'
    }
    print_joint_probability(network, joint_values)

    print('')

    conditionals_vars = {'High Consumption': 'true'}
    conditionals_evidents = {'Damaged Tire': 'false', 'Electronics Malfunctioning': 'false', 'Fuel Tank Leaking': 'true'}

    print_conditional_probability(network, conditionals_vars, conditionals_evidents)
    sample = create_random_sample(network)
    print_joint_probability(network, sample)


sprinkler()
