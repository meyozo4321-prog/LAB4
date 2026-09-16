# Candidate Elimination Algorithm
# Without using scikit-learn

# Training Dataset
data = [
    ["Sunny", "Warm", "Normal", "Strong", "Yes"],
    ["Sunny", "Warm", "High", "Strong", "Yes"],
    ["Rainy", "Cold", "High", "Strong", "No"],
    ["Sunny", "Warm", "High", "Weak", "Yes"]
]

attributes = ["Sky", "AirTemp", "Humidity", "Wind"]

# Most Specific Boundary
S = ["Ø", "Ø", "Ø", "Ø"]

# Most General Boundary
# IMPORTANT: G is a LIST OF HYPOTHESES
G = [["?", "?", "?", "?"]]


def print_hypothesis(h):
    return "<" + ", ".join(h) + ">"


def covers(hypothesis, instance):
    for h, value in zip(hypothesis, instance):
        if h != "?" and h != value:
            return False
    return True


def more_general_or_equal(h1, h2):
    for a, b in zip(h1, h2):
        if a != "?" and a != b:
            return False
    return True


def generalize_s(S, instance):
    new_S = S.copy()

    for i in range(len(S)):
        if S[i] == "Ø":
            new_S[i] = instance[i]

        elif S[i] != instance[i]:
            new_S[i] = "?"

    return new_S


def specialize_g(hypothesis, instance):

    domains = [
        ["Sunny", "Rainy"],
        ["Warm", "Cold"],
        ["Normal", "High"],
        ["Strong", "Weak"]
    ]

    specializations = []

    for i in range(len(hypothesis)):

        if hypothesis[i] == "?":

            for value in domains[i]:

                if value != instance[i]:

                    new_hypothesis = hypothesis.copy()
                    new_hypothesis[i] = value

                    specializations.append(new_hypothesis)

    return specializations


print("=" * 60)
print("CANDIDATE ELIMINATION ALGORITHM")
print("=" * 60)

print("\nAttributes:")
print(attributes)

print("\nInitial Boundaries:")
print("S =", print_hypothesis(S))
print("G =")

for g in G:
    print("  ", print_hypothesis(g))


# Process training examples
for step, row in enumerate(data, start=1):

    instance = row[:-1]
    target = row[-1]

    print("\n" + "-" * 60)
    print(f"Processing D{step}")
    print("-" * 60)

    print("Instance :", instance)
    print("Target   :", target)

    # --------------------------------------------------
    # POSITIVE INSTANCE
    # --------------------------------------------------
    if target == "Yes":

        # Generalize S
        S = generalize_s(S, instance)

        # Remove G hypotheses that don't cover positive example
        G = [
            g for g in G
            if covers(g, instance)
        ]

    # --------------------------------------------------
    # NEGATIVE INSTANCE
    # --------------------------------------------------
    else:

        new_G = []

        for g in G:

            if covers(g, instance):

                # Specialize G to exclude negative example
                specializations = specialize_g(g, instance)

                for h in specializations:

                    # Keep only hypotheses more general
                    # than or equal to S
                    if more_general_or_equal(h, S):
                        new_G.append(h)

            else:
                new_G.append(g)

        G = new_G

    # Remove hypotheses in G that are not
    # more general than S
    G = [
        g for g in G
        if more_general_or_equal(g, S)
    ]

    # Remove duplicate hypotheses
    unique_G = []

    for g in G:
        if g not in unique_G:
            unique_G.append(g)

    G = unique_G

    print("\nAfter processing D" + str(step) + ":")

    print("S =", print_hypothesis(S))

    print("G =")

    if len(G) == 0:
        print("   No hypotheses")
    else:
        for g in G:
            print("  ", print_hypothesis(g))


# --------------------------------------------------
# FINAL VERSION SPACE
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL VERSION SPACE")
print("=" * 60)

print("\nFinal Most Specific Boundary (S):")
print(print_hypothesis(S))

print("\nFinal Most General Boundary (G):")

for g in G:
    print(print_hypothesis(g))

print("\n" + "=" * 60)
print("Experiment Completed")
print("=" * 60)