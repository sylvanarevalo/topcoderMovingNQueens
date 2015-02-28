'''
representation

queens=[spot0,spot1,spot2,spot3...]
return ["queen# newQueenRow newQueenCol", "queen# newQueenRow newQueenCol"...]

I need to keep the queen order constant. It should be a queen list, and I should update it.
But I need to keep the order constant. Many functions need to be changed to reflect this.
'''


class MovingNQueens():
    def rearrange(queenRows, queenCols):
        return fullSolve(zip(queenRows,queenCols))

    def attackLines(queens):
        #Since I know there are at most 100 queens. Perhaps I don't want to use a hashtable.
        xs={}
        ys={}
        dus={}
        dds = {}
        for queen in queens:
            xs[queen[0]] =1+ xs.get(queen[0],0)
            ys[queen[1]] =1+ ys.get(queen[1],0)
            dus[queen[0]-queen[1]]=1+dus.get(queen[0]-queen[1],0)
            dds[queen[0]+queen[1]]=1+dds.get(queen[0]+queen[1],0)
        return (xs,ys,dus,dds)


    # In[32]:

    def considerMove(position,state):
        '''State = [queens, attackLines, moves, distance]
        considerMove returns the number of checks a queen who just moved to this position would be in.
        Returns inf if it is an illegal move
        But it doesn't actually check if the move is good. It needs to know where the queen came from as well.
        Otherwise we don't know if it is teleporting through other queens!
        '''
        if position in state[0]:
            return float("inf")
        xs, ys, dus, dds = state[1]
        return xs.get(position[0],0) + ys.get(position[1],0)+ dus.get(position[0]-position[1],0) + dds.get(position[0]+position[1],0) -1


    # In[33]:

    def numChecks(position,state):
        xs, ys, dus, dds = state[1]
        return xs.get(position[0],0) + ys.get(position[1],0)+ dus.get(position[0]-position[1],0) +     dds.get(position[0]+position[1],0) -4



    # In[34]:

    def isSolved(AL):
        #AL stands for attackLines, but I didn't want to name it the same as my function
        for dic in AL:
            if bool([a for a in dic.values() if a != 1]):
                     return False
        return True


    # In[35]:

    def adjacentSquares(p):
        return ((p[0]+1,p[1]),(p[0],p[1]+1),(p[0]+1,p[1]+1),(p[0]-1,p[1]),(p[0],p[1]-1),            (p[0]-1,p[1]+1),(p[0]+1,p[1]-1),(p[0]-1,p[1]-1))


    # In[36]:

    def moves(queen,state, considerTheseMoves):
        #
        nC= numChecks(queen,state)
        movelist=[]
        for pos in considerTheseMoves:
            moveval= considerMove(pos,state)
            if nC > moveval:
                movelist.append(((queen,pos),nC-moveval))
        return movelist





    # In[37]:

    def bestMove(state,bestMoveType):
        if bestMoveType==1:
            moveType= adjacentSquares
        else:
            moveType= lambda q: squaresxAway(q,bestMoveType)
        bestmove= (None,0)
        for queen in state[0]:
            for move in moves(queen,state,moveType(queen)):
                if move[1] > bestmove[1]:
                    bestmove=move
        if not bestmove[0] == None:
            return bestmove
        else:
            return bestMove(state,bestMoveType+1)




    # In[38]:

    def squaresxAway(p, x):
        #NOTE This doesn't make sure the move is valid, it could move through other queens
        return ((p[0]+x,p[1]),(p[0],p[1]+x),(p[0]+x,p[1]+x),(p[0]-x,p[1]),            (p[0],p[1]-x),(p[0]-x,p[1]+x),(p[0]+x,p[1]-x),(p[0]-x,p[1]-x))



    # In[39]:

    def makeMove(state,move):
        #State = [queens, AL, moves, distance]
        #move= ((start,end),val)
        queens, AL, moves, distance= state
        queens= list(queens)
        moves=list(moves)
        queens.remove(move[0][0])
        queens.append(move[0][1])
        #THESE TWO LINES ARE AWFUL. THEY MESS UP THE GLOBAL QUEENS OBJECT!
        #I SHOULD USE TUPLES IF I DON'T WANT MY STUFF MESSED WITH!
        #When I want to optimize more, then I can modify AL in a smart way, but for now:
        AL= attackLines(queens)
        moves.append(move[0])
        distance+= max(abs(move[0][0][0]-move[0][1][0]),abs(move[0][0][1]-move[0][1][1]))
        return (queens,AL,moves,distance)



    # In[40]:

    def solve(state):
        #pdb.set_trace()
        #State = [queens, attackLines, moves, distance]
        #if state[3] > bestSolution[1]:
        #    return None
        if isSolved(state[1]):
            #if distance < bestFoundDistance:
            #    bestSolution= (moves,distance)
            #print state
            #return locals()
            return state
        else:
            return solve(makeMove(state,bestMove(state,1)))



    # In[41]:

    def fullSolve(queens):
        import time
        import random
        #AL=attackLines(queens)
        #startingState= [queens,attackLines(queens),[],0]
        safty=2 #this is in case the last loop takes 6 times longer than my start loop.
        startTime= time.time()
        #parell solve many times:{
        bestSolution= solve([queens,attackLines(queens),[],0])
        #print bestSolution
        #bestSolution= solve([queens,attackLines(queens),[],0])
        #print bestSolution
        #}
        loopTime=startTime-time.time()
        while time.time()-startTime < 10-(safty*(loopTime) + 2):
            #parell solve many times:{
            queens= list(queens)
            random.shuffle(queens)
            current= solve((queens,attackLines(queens),[],0))
            if current[3]<bestSolution[3]:
                bestSolution=current
            #}
        return bestSolution

#________________
if __name__=="__main__":
    numQueens= input()
    queenRows=[]
    queenCols=[]
    for i in range(numQueens):
        queenRows.append(input())
# it just gives numQueens again
    input()
    for i in range(numQueens):
        queenCols.append(input())
    ret = rearrange(queenRows,queenCols)
    print(len(ret))
    for i in range(len(ret)):
        print ret[i]
    import sys
    sys.stdout.flush()

# len = parseInt(readLine())
#     for (i=0; i < len; i++)
#         queenRows[i] = parseInt(readLine())
#
#     len = parseInt(readLine())
#     for (i=0; i < len; i++)
#         queenCols[i] = parseInt(readLine())
#
#     ret = rearrange(queenRows, queenCols)
#
# printLine(length(ret[i]))
#     for (i=0; i < length(ret[i]); i++)
#         printLine(ret[i])
#
# flush(stdout)
#
