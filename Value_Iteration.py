import time
start = time.time()

def Take_Input_And_Initialize():
    global Walls, Rewards, Walls_list, Rewards_list, Matrix_probabilities, Prob_list, Utility, P, Rp, Df, \
        Non_Wall_And_Reward_Positions, Size, Travel_Policy, Neighbours, Neighbours_list, Non_Terminal_Positions

    Neighbours = {}

    Walls = {}
    Rewards = {}
    Walls_list = []
    Rewards_list = []
    Neighbours = {}
    Matrix_probabilities = {}
    Prob_list = []
    Non_Wall_And_Reward_Positions = []
    f = open("input4.txt", "r")

    lines = f.readlines()

    Size = int(lines[0])

    Number_of_walls = int(lines[1])
    for i in range(2, Number_of_walls + 2):
        Wall_position = lines[i].split(",")
        x = int(Wall_position[0])
        y = int(Wall_position[1])
        Walls[(x, y)] = 0
        Walls_list.append((x, y))
    Reward_states = int(lines[1 + Number_of_walls + 1])

    loop_start = 1 + Number_of_walls + 2

    for i in range(loop_start, loop_start + Reward_states):
        Reward_position = lines[i].split(",")
        x = int(Reward_position[0])
        y = int(Reward_position[1])
        Rewards[(x, y)] = float(Reward_position[2])
        Rewards_list.append((x, y))

    P = float(lines[loop_start + Reward_states])
    Rp = float(lines[loop_start + Reward_states + 1])
    Df = float(lines[loop_start + Reward_states + 2])

    Travel_Policy = [['' for _ in range(Size)] for _ in range(Size)]

    Utility = [[0.0 for _ in range(Size + 2)] for _ in range(Size + 2)]

    for i in range(0, len(Walls_list)):
        Utility[Walls_list[i][0]][Walls_list[i][1]] = 0
        Travel_Policy[Walls_list[i][0] - 1][Walls_list[i][1] - 1] = "N"

    for i in range(0, len(Rewards_list)):
        Utility[Rewards_list[i][0]][Rewards_list[i][1]] = Rewards[(Rewards_list[i][0], Rewards_list[i][1])]
        Travel_Policy[Rewards_list[i][0] - 1][Rewards_list[i][1] - 1] = "E"

    for i in range(1, Size + 1):
        for j in range(1, Size + 1):
            if (Travel_Policy[i - 1][j - 1] == ""):
                Utility[i][j] = Rp
                pos = (i, j)
                Non_Wall_And_Reward_Positions.append(pos)
    Non_Terminal_Positions = set(Non_Wall_And_Reward_Positions)


def Determine_Neighbours():
    for pos in Non_Wall_And_Reward_Positions:
        Neighbours_list = []
        i = pos[0]
        j = pos[1]

        N = (i - 1, j)
        W = (i, j - 1)
        E = (i, j + 1)
        S = (i + 1, j)
        NW = (i - 1, j - 1)
        NE = (i - 1, j + 1)
        SW = (i + 1, j - 1)
        SE = (i + 1, j + 1)
        if NW not in Walls and NW not in Rewards and not NW[0] == 0 and not NW[1] == 0:
            Neighbours_list.append(NW)
        if N not in Walls and N not in Rewards and not N[0] == 0:
            Neighbours_list.append(N)
        if NE not in Walls and NE not in Rewards and not NE[0] == 0 and not NE[1] == Size + 1:
            Neighbours_list.append(NE)
        if W not in Walls and not W in Rewards and not W[1] == 0:
            Neighbours_list.append(W)
        if E not in Walls and E not in Rewards and not E[1] == Size + 1:
            Neighbours_list.append(E)
        if S not in Walls and S not in Rewards and not S[0] == Size + 1:
            Neighbours_list.append(S)
        if SW not in Walls and SW not in Rewards and not SW[0] == Size + 1 and not SW[1] == 0:
            Neighbours_list.append(SW)
        if SE not in Walls and SE not in Rewards and not SE[0] == Size + 1 and not SE[1] == Size + 1:
            Neighbours_list.append(SE)

        Neighbours[pos] = Neighbours_list


def Calculate_And_Map_Probabilities():
    for pos in Non_Wall_And_Reward_Positions:
        Probability_list = []
        i = pos[0]
        j = pos[1]

        N = (i - 1, j)
        W = (i, j - 1)
        E = (i, j + 1)
        S = (i + 1, j)
        NW = (i - 1, j - 1)
        NE = (i - 1, j + 1)
        SW = (i + 1, j - 1)
        SE = (i + 1, j + 1)

        C_N = 0
        C_S = 0
        C_E = 0
        C_W = 0

        if N in Walls or N[0] == 0:
            N_P = 0
            C_N += P
        else:
            N_P = P
        if NE in Walls or NE[0] == 0 or NE[1] == Size + 1:
            NE_P = 0
            C_N += (1 - P) / 2
            C_E += (1 - P) / 2
        else:
            NE_P = (1 - P) / 2
        if NW in Walls or NW[0] == 0 or NW[1] == 0:
            NW_P = 0
            C_N += (1 - P) / 2
            C_W += (1 - P) / 2

        else:
            NW_P = (1 - P) / 2

        if S in Walls or S[0] == Size + 1:
            S_P = 0
            C_S += P
        else:
            S_P = P
        if SE in Walls or SE[0] == Size + 1 or SE[1] == Size + 1:
            SE_P = 0
            C_S += (1 - P) / 2
            C_E += (1 - P) / 2
        else:
            SE_P = (1 - P) / 2

        if SW in Walls or SW[0] == Size + 1 or SW[1] == 0:
            SW_P = 0
            C_S += (1 - P) / 2
            C_W += (1 - P) / 2
        else:
            SW_P = (1 - P) / 2

        if W in Walls or W[1] == 0:
            W_P = 0
            C_W += P
        else:
            W_P = P

        if E in Walls or E[1] == Size + 1:
            E_P = 0
            C_E += P
        else:
            E_P = P

        Probability_list.append(N_P)
        Probability_list.append(S_P)
        Probability_list.append(W_P)
        Probability_list.append(E_P)
        Probability_list.append(NW_P)
        Probability_list.append(NE_P)
        Probability_list.append(SW_P)
        Probability_list.append(SE_P)
        Probability_list.append(C_N)
        Probability_list.append(C_S)
        Probability_list.append(C_W)
        Probability_list.append(C_E)

        Matrix_probabilities[pos] = Probability_list


def Calculate_Utility_And_Travel_Policy():
    global Non_Terminal_Positions
    Epsilon = 0.0001 * (1 - Df) / (2 * Df)
    Maximum_Difference = 1.0
    while Non_Terminal_Positions and Maximum_Difference > Epsilon:
        Maximum_Difference = float("-inf")
        Non_Wall_And_Reward_States = list(Non_Terminal_Positions)
        Non_Terminal_Positions = set()
        for pos in Non_Wall_And_Reward_States:
            i = pos[0]
            j = pos[1]

            Prob_list = Matrix_probabilities[pos]
            Neighours_list = Neighbours[pos]

            N_P = Prob_list[0]
            S_P = Prob_list[1]
            W_P = Prob_list[2]
            E_P = Prob_list[3]
            NW_P = Prob_list[4]
            NE_P = Prob_list[5]
            SW_P = Prob_list[6]
            SE_P = Prob_list[7]
            C_N = Prob_list[8]
            C_S = Prob_list[9]
            C_W = Prob_list[10]
            C_E = Prob_list[11]
            N_Utility = N_P * Utility[i - 1][j] + NW_P * Utility[i - 1][j - 1] + NE_P * Utility[i - 1][j + 1] + C_N * \
                        Utility[i][j]

            S_Utility = S_P * Utility[i + 1][j] + SW_P * Utility[i + 1][j - 1] + SE_P * Utility[i + 1][j + 1] + C_S * \
                        Utility[i][j]

            W_Utility = W_P * Utility[i][j - 1] + NW_P * Utility[i - 1][j - 1] + SW_P * Utility[i + 1][j - 1] + C_W * \
                        Utility[i][j]

            E_Utility = E_P * Utility[i][j + 1] + NE_P * Utility[i - 1][j + 1] + SE_P * Utility[i + 1][j + 1] + C_E * \
                        Utility[i][j]
            Max_Utility = max(N_Utility, S_Utility, W_Utility, E_Utility)

            old_Utility = Utility[i][j]
            new_Utility = (Max_Utility * Df) + Rp
            if Max_Utility == N_Utility:
                Travel_Policy[i - 1][j - 1] = 'U'
            elif Max_Utility == S_Utility:
                Travel_Policy[i - 1][j - 1] = 'D'
            elif Max_Utility == W_Utility:
                Travel_Policy[i - 1][j - 1] = 'L'
            elif Max_Utility == E_Utility:
                Travel_Policy[i - 1][j - 1] = 'R'

            if new_Utility > old_Utility:
                Maximum_Difference = max(Maximum_Difference, abs(new_Utility - old_Utility))
                for state in Neighours_list:
                    Non_Terminal_Positions.add(state)
            Utility[i][j] = new_Utility

    file_output = open('output.txt', mode="w+")
    for i in range(Size):
        for j in range(Size):
            file_output.write(Travel_Policy[i][j])
            if j != Size - 1:
                file_output.write(",")
        if i != Size - 1:
            file_output.write("\n")
    file_output.close()


def main():
    Take_Input_And_Initialize()
    Calculate_And_Map_Probabilities()
    Determine_Neighbours()

    Calculate_Utility_And_Travel_Policy()
    end = time.time()
    print("Total time taken", end - start)

if __name__ == '__main__':
    main()