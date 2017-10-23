from pypelt.fuzzy_classes import FuzzyKB


def fuzzify(inputs: list, kb: FuzzyKB) -> dict:
    """
    gets crisp input from parser and queries the KB for memberships of respective sets in variable domains
    :param inputs: list of crisp inputs
    :param kb: the fuzzy knowledgebase singleton
    :return: dictionary with antecedent set memberships
    """
    pelt = {}
    for entry in inputs:  # query kb for fuzzy values based on crisp inputs for antecedent sets
        pelt.update(kb.parse_query(entry[0], float(entry[1])))

    return pelt
