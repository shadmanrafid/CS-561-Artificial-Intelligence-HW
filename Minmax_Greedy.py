import copy
import time
start = time.time()

def find_score(pos, state, player, score, r, c, iteration, N):
    if iteration==3:
        return score
    if pos[0] + r >= 0 and pos[0] + r < N and pos[1] + c >= 0 and pos[1] + c < N:
        if state[pos[0]+r][pos[1]+c] == 0:
            state[pos[0] + r][pos[1] + c] = player
            score = score + 1
        elif state[pos[0]+r][pos[1]+c] == player or state[pos[0]+r][pos[1]+c] == 4:
            score = score
        elif state[pos[0]+r][pos[1]+c] != player and state[pos[0]+r][pos[1]+c] != 3:
            state[pos[0] + r][pos[1] + c] = 4
            score = score + 1
        else:
            return score

    return find_score((pos[0]+r, pos[1]+c), state, player, score, r, c, iteration+1, N)



def root_start(table, alpha, beta, N):
    max_utility=-1000000
    best_move=(0,0)

    score1 = 0
    score2 = 0

    temp_table = copy.deepcopy(table)

    for i in range(0,N):
        for j in range(0,N):
            if table[i][j]==1:
                player = 1
                score1 = score1 + 1
                score1 = score1 + find_score((i,j), temp_table, player, 0, 0, 1, 0, N)
                score1 = score1 + find_score((i,j), temp_table, player, 0, 0, -1, 0, N)
                score1 = score1 + find_score((i,j), temp_table, player, 0, 1, 0, 0, N)
                score1 = score1 + find_score((i,j), temp_table, player, 0, -1, 0, 0, N)
                score1 = score1 + find_score((i,j), temp_table, player, 0, -1, -1, 0, N)
                score1 = score1 + find_score((i,j), temp_table, player, 0, -1, 1, 0, N)
                score1 = score1 + find_score((i,j), temp_table, player, 0, 1, -1, 0, N)
                score1 = score1 + find_score((i,j), temp_table, player, 0, 1, 1, 0, N)
            elif table[i][j]==2:
                player = 2
                score2 = score2 + 1
                score2 = score2 + find_score((i,j), temp_table, player, 0, 0, 1, 0, N)
                score2 = score2 + find_score((i,j), temp_table, player, 0, 0, -1, 0, N)
                score2 = score2 + find_score((i,j), temp_table, player, 0, 1, 0, 0, N)
                score2 = score2 + find_score((i,j), temp_table, player, 0, -1, 0, 0, N)
                score2 = score2 + find_score((i,j), temp_table, player, 0, -1, -1, 0, N)
                score2 = score2 + find_score((i,j), temp_table, player, 0, -1, 1, 0, N)
                score2 = score2 + find_score((i,j), temp_table, player, 0, 1, -1, 0, N)
                score2 = score2 + find_score((i,j), temp_table, player, 0, 1, 1, 0, N)

    for i in range(0,N):
        for j in range(0,N):
            if temp_table[i][j]==0:
                table_copy=copy.deepcopy(temp_table)
                table_copy[i][j]=1
                # print("Print 1st time --->")
                # print(table_copy)
                utility=evaluate(N, table_copy, (i,j), 1, score1 + 1, score2, alpha, beta)

                if utility >= max_utility:
                    max_utility=utility
                    best_move=(i,j)

                if max_utility >= alpha:
                    alpha = max_utility

                if alpha >= beta:
                    break
                # print("Print 2ns time -->")
                # print(table_copy)
    return  max_utility, best_move

def evaluate(N, state, pos, player, score1, score2, alpha, beta, depth=1, maxdepth=5):
    if player==1:
        score1 = score1 + find_score(pos, state, player, 0, 0, 1, 0, N)
        score1 = score1 + find_score(pos, state, player, 0, 0, -1, 0, N)
        score1 = score1 + find_score(pos, state, player, 0, 1, 0, 0, N)
        score1 = score1 + find_score(pos, state, player, 0, -1, 0, 0, N)
        score1 = score1 + find_score(pos, state, player, 0, -1, -1, 0, N)
        score1 = score1 + find_score(pos, state, player, 0, -1, 1, 0, N)
        score1 = score1 + find_score(pos, state, player, 0, 1, -1, 0, N)
        score1 = score1 + find_score(pos, state, player, 0, 1, 1, 0, N)



        if depth == maxdepth:
            return score1 - score2
            #return the list as well

        min_utility = 1000000
        game_over = True
        for i in range(0, N):
            for j in range(0, N):
                if state[i][j] == 0:
                    game_over = False
                    table_copy = copy.deepcopy(state)
                    table_copy[i][j] = 2
                    utility = evaluate(N, table_copy, (i, j), 2, score1, score2 + 1, alpha, beta, depth + 1)

                    ##Where the revrsion takes place

                    if utility <= min_utility:
                        min_utility = utility

                    if min_utility <= beta:
                        beta = min_utility

                    if alpha >= beta:
                        break

        if game_over == True:
            return score1 - score2
        #return the list as well

        return min_utility
        #return the list as well

    elif player==2:
        score2 = score2 + find_score(pos, state, player, 0, 0, 1, 0, N)
        score2 = score2 + find_score(pos, state, player, 0, 0, -1, 0, N)
        score2 = score2 + find_score(pos, state, player, 0, 1, 0, 0, N)
        score2 = score2 + find_score(pos, state, player, 0, -1, 0, 0, N)
        score2 = score2 + find_score(pos, state, player, 0, -1, -1, 0, N)
        score2 = score2 + find_score(pos, state, player, 0, -1, 1, 0, N)
        score2 = score2 + find_score(pos, state, player, 0, 1, -1, 0, N)
        score2 = score2 + find_score(pos, state, player, 0, 1, 1, 0, N)


        if depth == maxdepth:
            return score1 - score2

        max_utility = -1000000

        game_over = True
        for i in range(0, N):
            for j in range(0, N):
                if state[i][j] == 0:
                    game_over = False
                    table_copy = copy.deepcopy(state)
                    table_copy[i][j] = 1
                    utility = evaluate(N, table_copy, (i, j), 1, score1 + 1, score2, alpha, beta, depth + 1)

                    if utility >= max_utility:
                        max_utility = utility

                    if max_utility >= alpha:
                        alpha = max_utility

                    if alpha >= beta:
                        break

        if game_over == True:
            return score1 - score2

        return max_utility


f=open("input3.txt", "r")
lines=f.readlines()

N=int(lines[0])
table=[0]*N
for i in range(1,N+1):
     table[i-1]=[int(k) for k in list(lines[i][0:N])]

'''
state= table
player =1
pos = (3,2)
print find_score(pos, table, player, 0, 0, 1, 0, N)
print find_score(pos, state, player, 0, 0, -1, 0, N)
print find_score(pos, state, player, 0, 1, 0, 0, N)
print find_score(pos, state, player, 0, -1, 0, 0, N)
print find_score(pos, state, player, 0, -1, -1, 0, N)
print find_score(pos, state, player, 0, -1, 1, 0, N)
print find_score(pos, state, player, 0, 1, -1, 0, N)
print find_score(pos, state, player, 0, 1, 1, 0, N)
'''
answer = root_start(table, -1000000, 1000000, N)
f.close()

f2=open("output.txt", "w")
f2.write('%d %d' %(answer[1][0], answer[1][1]))
f2.close()

end = time.time()
print(format(end - start, '.10f'))