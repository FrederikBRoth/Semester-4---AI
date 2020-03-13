A = "A"
B = "B"
C = "C"
D = "D"

Environment = {
    A: "Dirty",
    B: "Dirty",
    C: "Clean",
    D: "Dirty",
    "Current": A
}

def REFLEX_VACUUM_AGENT(loc_st):
    if loc_st[1] == "Dirty":
        return "Suck"
    if loc_st[0] == A:
        return "Right"
    if loc_st[0] == B:
        return "Right"
    if loc_st[0] == C:
        return "Right"
    if loc_st[0] == D:
        return "Right"

def Sensors():
    location = Environment["Current"]
    return (location, Environment[location])

def Actuators(action):
    location = Environment["Current"]
    if action == "Suck":
        Environment[location] = "Clean"
    elif action == "Right" and location == A:
        Environment["Current"] = B
    elif action == "Right" and location == B:
        Environment["Current"] = C
    elif action == "Right" and location == C:
        Environment["Current"] = D
    elif action == "Right" and location == D:
        Environment["Current"] = A

def run(n, make_agent):
    print("    Current                           New")
    print("location    status   action  location    status")
    for i in range(1, n):
        (location, status) =Sensors()
        print("{:12s}{:8s}".format(location, status), end="")
        action = make_agent(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:12s}{:8s}{:12s}".format(action, location, status))


run(20, REFLEX_VACUUM_AGENT)

#Question: While it runs it does not give correct information