import epispot as epi
import numpy as np # lgtm [py/unused-import]
from copy import deepcopy


def predict_short_term(case_data, entries, initial, end, n, time):

    """
    Use this for short-term predictions only.
    Long-term predictions may be inaccurate due to the prediction mechanism used.
    Constructs an SIR Model to track the growth of cases given a predicted R Naught value and initial recovered
    population from the data

    :param case_data: Past case data organized earliest-latest (preferrably from the last 30 days)
    :param entries: Number of entries in the case_data file
    :param initial: Initial cases (at start of case_data)
    :param end: Final number of cases (at end of case_data)
    :param n: Total population of the region in question
    :param time: Time for prediction (in days)
    :return: Predicted cases
    """

    def build_model(params):

        """
        Builds a new epispot model and returns results.
        Used for parameter fitting.
        Several parameters have been pre-fitted from existing data.
        """

        r_0 = params[0]
        initial_recovered = params[1]

        # Parameter Definitions

        def N(t):
            return n

        def R_0(t):
            return r_0

        def gamma(t):
            return 1 / 8.89375

        def p_rec(t):
            return 1.0

        def rec_rate(t):
            return 1 / 23

        # Model Build
        """
        S --> I --> R
        """

        Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
        Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_rec, recovery_rate=rec_rate)
        Recovered = epi.comps.Recovered(2, p_from_inf=p_rec, from_inf_rate=rec_rate)

        # Model Compiler
        Compiled_Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Recovered],
                                          layer_names=['Susceptible', 'Infected', 'Recovered'],
                                          layer_map=[[Infected], [Recovered], []])

        # Model Output
        initial_vector = [n - initial - initial_recovered, initial, initial_recovered]
        result = Compiled_Model.integrate(range(0, entries), starting_state=initial_vector)

        formatted = []
        for system in result:
            formatted.append([deepcopy(system)[1]])

        return formatted

    def compile_model(params):

        """
        Builds a new epispot model and returns results.
        Used for parameter fitting.
        Several parameters have been pre-fitted from existing data.
        """

        r_0 = params[0]

        # Parameter Definitions

        def N(t):
            return n

        def R_0(t):
            return r_0

        def gamma(t):
            return 1 / 8.89375

        def p_rec(t):
            return 1.0

        def rec_rate(t):
            return 1 / 23

        # Model Build
        """
        S --> I --> R
        """

        Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
        Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_rec, recovery_rate=rec_rate)
        Recovered = epi.comps.Recovered(2, p_from_inf=p_rec, from_inf_rate=rec_rate)

        # Model Compiler
        Compiled_Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Recovered],
                                          layer_names=['Susceptible', 'Infected', 'Recovered'],
                                          layer_map=[[Infected], [Recovered], []])

        return Compiled_Model

    params_to_build = [0.007 * n, 2.0]
    # optimized_parameters = epi.fitters.grad_des(build_model, case_data, params_to_build,
                                               # 0.3, 5, n, range(entries))
    ranges = [[0.0 + 0.25 * k for k in range(11)], [0.0 + 0.001 * n * k for k in range(22)]]
    optimized_parameters = epi.fitters.tree_search(build_model, case_data, params_to_build, ranges, 3, n,
                                                   range(entries), verbose=False)

    print('\nOptimization complete. A verbose log of the optimized parameters is shown below.')
    print(optimized_parameters)

    Model = compile_model(optimized_parameters)
    print('\nModel compiled.')

    R_0 = optimized_parameters[0] # lgtm [py/unused-local-variable]
    initial_recovered = optimized_parameters[1]

    predictions = Model.integrate(range(0, time),
                 starting_state=[n - end - initial_recovered, end, initial_recovered])

    return predictions[-1][1]


def predict_uncontrolled(total_cases, current_cases, n, time):

    """
    Predict the uncontrolled spread of COVID-19 over a set amount of time

    :param total_cases: total confirmed COVID-19 cases
    :param current_cases: number of currently infectious persons
    :param n: total population
    :param time: Time to predict (in days)
    :return: cases after `time` days
    """

    def N(t):
        return n

    def R_0(t):
        return 2.5

    def gamma(t):
        return 1 / 8.89375

    def p_rec(t):
        return 1.0

    def rec_rate(t):
        return 1 / 23

    # Model Build
    """
    S --> I --> R
    """

    Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)
    Infected = epi.comps.Infected(1, N, R_0=R_0, gamma=gamma, p_recovery=p_rec, recovery_rate=rec_rate)
    Recovered = epi.comps.Recovered(2, p_from_inf=p_rec, from_inf_rate=rec_rate)

    # Model Compiler
    Compiled_Model = epi.models.Model(N(0), layers=[Susceptible, Infected, Recovered],
                                      layer_names=['Susceptible', 'Infected', 'Recovered'],
                                      layer_map=[[Infected], [Recovered], []])
    result = Compiled_Model.integrate(range(0, time + 1),
                                      starting_state=[n - total_cases, current_cases, total_cases - current_cases])
    return round(result[-1][1])  # most recent, infected category

# predict short term
"""
data = open('test-data/sf-total-cases.csv')  # .readlines()
# cases = [data[l].split(',')[1] for l in range(len(data))][-30:]

print(predict_short_term(data, 30, 2766, 4430, 883305, 7))
"""

# predict uncontrolled
# print(predict_uncontrolled(94315331, 24950778, 7e9, 1))
