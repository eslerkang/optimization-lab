PROBLEM_DIMENSION = "low" or "high"
INITIAL_END_POINT_TYPE = "fixed" or "random"
PHEROMONE = True or False
WAGGLE = True or False


def algorithm():
    if PROBLEM_DIMENSION == "low":
        if INITIAL_END_POINT_TYPE == "fixed":
            if WAGGLE:
                return "BEE"
            else:
                return "ACO"
        elif INITIAL_END_POINT_TYPE == "random":
            return "TABU"
    else:
        return "RANDOM WALK"
