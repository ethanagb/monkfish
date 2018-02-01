#MONKFISH v 0.1
#eagb@mit.edu

import pandas as pd
import numpy as np
from random import shuffle
print("\nLoading data...\n")

##################################################
###YOU CAN CHANGE THE NAME OF DATA FILE HERE!!!###
data = pd.read_csv('preferences.csv', header=0)###
##################################################

####################
##SET THE CAP HERE##
cap = 3
####################

dinner = data.loc[:,'Name':'VeggieGalaxy']
brunch = data.loc[:,'Area4':]
names = data['Name']
brunch = pd.concat([names,brunch], axis=1)

print("The attendance cap is currently set at " + str(cap) + ".\n")

kika = []
thelonious = []
smokeshop =[]
ole = []
meadhall = []
indiapav = []
veggieGalaxy = []
names = data['Name'].tolist()
assigned = []
unassigned = []

assignmentLists = [kika,thelonious,smokeshop,ole,meadhall,indiapav,veggieGalaxy]
restaurantNames = dinner.columns[1:].tolist()
assignmentDict = dict(zip(restaurantNames, assignmentLists))
zeroes = [0]*len(names)
preferenceScoreDict = dict(zip(names, zeroes))

for col in dinner.columns[1:]:
    d = dinner[col]
    i = 0
    while i < len(d):
        if d[i] == 1:
            #assign first preference
            assignmentDict[col].append(names[i])
            #mark the person as assigned.
            assigned.append(names[i])
            #update the person's cumulative preference score
            preferenceScoreDict[names[i]] += 1
        i += 1
#Now all first choices have been granted, check whether any restaurants are over capacity
def dinnerCapacityCheck():
    dinnerOverassigned = []
    dinnerUnderassigned = []
    dinnerFull = []
    for rest in restaurantNames:
        if len(assignmentDict[rest]) > cap:
            print(str(rest) + ' is overassigned')
            dinnerOverassigned.append(rest)
        elif len(assignmentDict[rest]) < cap:
            print(str(rest) + ' is underassigned')
            dinnerUnderassigned.append(rest)
        elif len(assignmentDict[rest]) == cap:
            print(str(rest) + ' is full')
            dinnerFull.append(rest)
    return dinnerOverassigned, dinnerUnderassigned, dinnerFull
dinnerOverassigned, dinnerUnderassigned, dinnerFull = dinnerCapacityCheck()
dinnerDone=False
if len(dinnerOverassigned) == 0:
    #everyone gets their first choice, ideal solution.
    dinnerDone = True
    for name in restaurantNames:
        print("The following have been assigned to " + str(name) + ":")
        for x in assignmentDict[name]:
            print(str(x) + '\n')
elif len(dinnerOverassigned) > 0:
    #some people will have to be reassigned.
    #for each overassigned restaurant, randomly choose the number of people required to kick out to go below the cap
    for rest in dinnerOverassigned:
        dinnerList = assignmentDict[rest]
        bumpNum = len(dinnerList)-cap
        gotBumped = np.random.choice(dinnerList, bumpNum)
        for b in gotBumped:
            assignmentDict[rest].remove(b) #kick that dude out
            assigned.remove(b) #mark them unassigned
            unassigned.append(b)
            preferenceScoreDict[b] += 1 #increment their preference score
        #assign bumped people to their second choice.
        for x in unassigned:
            if x in assigned:
                print(str(x) + " is already assigned.")
                unassigned.remove(x)
                continue
            i = names.index(x)
            row = dinner.ix[i] #this should be the row of the the bumped person
            #reassign them to their second choice
            j=0
            #find the row index of this person who must be reassigned.
            while j < len(dinner['Name']):
                if dinner['Name'][j] == x:
                    break
                j += 1
            #Search for which restaurant was their second choice.
            for col in dinner.columns[1:]:
                d = dinner[col][j]
                if d == 2:
                    #assign second preference
                    assignmentDict[col].append(names[j])
                    #mark the person as assigned.
                    if names[j] not in assigned:
                        assigned.append(names[j])
        for a in assigned:
            if a in unassigned:
                unassigned.remove(a)
    dinnerOverassigned, dinnerUnderassigned, dinnerFull = dinnerCapacityCheck()

#now second choices have been assigned.
if len(dinnerOverassigned) == 0 and dinnerDone==False:
    dinnerDone = True
    for name in restaurantNames:
        print("The following have been assigned to " + str(name) + ":")
        for x in assignmentDict[name]:
            print(str(x) + '\n')
#consider bumping people to third choice.
elif len(dinnerOverassigned) > 0 and dinnerDone==False:
    #some people will have to be reassigned.
    #for each overassigned restaurant, randomly choose the number of people required to kick out to go below the cap
    for rest in dinnerOverassigned:
        dinnerList = assignmentDict[rest]
        bumpNum = len(dinnerList)-cap
        bumpOrder = random.shuffle(dinnerList) #want to preferentially bump people who haven't yet been bumped.
        gotBumped = []
        for x in bumpOrder:
            if len(gotBumped) == bumpNum:
                break
            if preferenceScoreDict[x] == 1:
                gotBumped.append(x)
            else:
                continue
        for b in gotBumped:
            assignmentDict[rest].remove(b) #kick that dude out
            assigned.remove(b) #mark them unassigned
            unassigned.append(b)
            preferenceScoreDict[b] += 1 #increment their preference score
        #assign bumped people to their second choice.
        for x in unassigned:
            if x in assigned:
                print(str(x) + " is already assigned.")
                unassigned.remove(x)
                continue
            i = names.index(x)
            row = dinner.ix[i] #this should be the row of the the bumped person
            #reassign them to their second choice
            j=0
            #find the row index of this person who must be reassigned.
            while j < len(dinner['Name']):
                if dinner['Name'][j] == x:
                    break
                j += 1
            #Search for which restaurant was their third choice.
            for col in dinner.columns[1:]:
                d = dinner[col][j]
                if d == 3:
                    #assign second preference
                    assignmentDict[col].append(names[j])
                    #mark the person as assigned.
                    if names[j] not in assigned:
                        assigned.append(names[j])
        for a in assigned:
            if a in unassigned:
                unassigned.remove(a)

    dinnerOverassigned, dinnerUnderassigned, dinnerFull = dinnerCapacityCheck()
    #if still overassigned after the second choice, run the brunch algorithm
    #then minimize preference scores as a last resort.
if len(dinnerOverassigned) == 0 and dinnerDone==False:
    dinnerDone = True
    for name in restaurantNames:
        print("The following have been assigned to " + str(name) + ":")
        for x in assignmentDict[name]:
            print(str(x) + '\n')
####START OF BRUNCH###
print("\nBeep Boop...assigning brunches...boop beep\n")
Area4 = []
PaintedBurro = []
RusselHouse =[]
Christophers = []
Ryles = []
CambridgeCommons = []

assigned = []
unassigned = []

assignmentLists = [Area4,PaintedBurro,RusselHouse,Christophers,Ryles,CambridgeCommons]
restaurantNames = brunch.columns[1:].tolist()
assignmentDict = dict(zip(restaurantNames, assignmentLists))

for col in brunch.columns[1:]:
    d = brunch[col]
    i = 0
    while i < len(d):
        if d[i] == 1:
            #assign first preference
            assignmentDict[col].append(names[i])
            #mark the person as assigned.
            assigned.append(names[i])
            #update the person's cumulative preference score
            preferenceScoreDict[names[i]] += 1
        i += 1
#Now all first choices have been granted, check whether any restaurants are over capacity
def brunchCapacityCheck():
    brunchOverassigned = []
    brunchUnderassigned = []
    brunchFull = []
    for rest in restaurantNames:
        if len(assignmentDict[rest]) > cap:
            print(str(rest) + ' is overassigned')
            brunchOverassigned.append(rest)
        elif len(assignmentDict[rest]) < cap:
            print(str(rest) + ' is underassigned')
            brunchUnderassigned.append(rest)
        elif len(assignmentDict[rest]) == cap:
            print(str(rest) + ' is full')
            brunchFull.append(rest)
    return brunchOverassigned, brunchUnderassigned, brunchFull
brunchOverassigned, brunchUnderassigned, brunchFull = brunchCapacityCheck()
brunchDone=False
if len(brunchOverassigned) == 0:
    #everyone gets their first choice, ideal solution.
    brunchDone = True
    for name in restaurantNames:
        print("The following have been assigned to " + str(name) + ":")
        for x in assignmentDict[name]:
            print(str(x) + '\n')
elif len(brunchOverassigned) > 0:
    #some people will have to be reassigned.
    #for each overassigned restaurant, randomly choose the number of people required to kick out to go below the cap
    for rest in brunchOverassigned:
        brunchList = assignmentDict[rest]
        bumpNum = len(brunchList)-cap
        gotBumped = np.random.choice(brunchList, bumpNum)
        for b in gotBumped:
            assignmentDict[rest].remove(b) #kick that dude out
            assigned.remove(b) #mark them unassigned
            unassigned.append(b)
            preferenceScoreDict[b] += 1 #increment their preference score
        #assign bumped people to their second choice.
        for x in unassigned:
            if x in assigned:
                print(str(x) + " is already assigned.")
                unassigned.remove(x)
                continue
            #print(x)
            i = names.index(x)
            row = brunch.ix[i] #this should be the row of the the bumped person
            #reassign them to their second choice
            j=0
            #find the row index of this person who must be reassigned.
            while j < len(brunch['Name']):
                if brunch['Name'][j] == x:
                    break
                j += 1
            #Search for which restaurant was their second choice.
            for col in brunch.columns[1:]:
                d = brunch[col][j]
                if d == 2:
                    #assign second preference
                    assignmentDict[col].append(names[j])
                    #mark the person as assigned.
                    if names[j] not in assigned:
                        assigned.append(names[j])
        for a in assigned:
            if a in unassigned:
                unassigned.remove(a)

    brunchOverassigned, brunchUnderassigned,brunchFull = brunchCapacityCheck()

if len(brunchOverassigned) == 0 and brunchDone==False:
    brunchDone = True
    for name in restaurantNames:
        print("The following have been assigned to " + str(name) + ":")
        for x in assignmentDict[name]:
            print(str(x) + '\n')

#consider bumping people to third choice.
elif len(brunchOverassigned) > 0 and brunchDone==False:
    #some people will have to be reassigned.
    #for each overassigned restaurant, randomly choose the number of people required to kick out to go below the cap
    for rest in brunchOverassigned:
        brunchList = assignmentDict[rest]
        bumpNum = len(brunchList)-cap
        bumpOrder = random.shuffle(brunchList) #want to preferentially bump people who haven't yet been bumped.
        gotBumped = []
        for x in bumpOrder:
            if len(gotBumped) == bumpNum:
                break
            if preferenceScoreDict[x] == 1:
                gotBumped.append(x)
            else:
                continue
        if len(gotBumped) < bumpNum:
            for x in bumpOrder:
                if len(gotBumped) == bumpNum:
                    break
                if preferenceScoreDict[x] == 2:
                    gotBumped.append(x)
                else:
                    continue
        if len(gotBumped) < numpNum:
            for x in bumpOrder:
                if len(gotBumped) == bumpNum:
                    break
                if preferenceScoreDict[x] == 3:
                    gotBumped.append(x)
                else:
                    continue
        for b in gotBumped:
            assignmentDict[rest].remove(b) #kick that dude out
            assigned.remove(b) #mark them unassigned
            unassigned.append(b)
            preferenceScoreDict[b] += 1 #increment their preference score
        #assign bumped people to their third choice.
        for x in unassigned:
            if x in assigned:
                print(str(x) + " is already assigned.")
                unassigned.remove(x)
                continue
            #print(x)
            i = names.index(x)
            row = brunch.ix[i] #this should be the row of the the bumped person
            #reassign them to their second choice
            j=0
            #find the row index of this person who must be reassigned.
            while j < len(brunch['Name']):
                if brunch['Name'][j] == x:
                    break
                j += 1
            #Search for which restaurant was their third choice.
            for col in brunch.columns[1:]:
                d = brunch[col][j]
                if d == 3:
                    #assign second preference
                    assignmentDict[col].append(names[j])
                    #mark the person as assigned.
                    if names[j] not in assigned:
                        assigned.append(names[j])
        for a in assigned:
            if a in unassigned:
                unassigned.remove(a)
    brunchOverassigned, brunchUnderassigned, brunchFull = brunchCapacityCheck()
if len(brunchOverassigned) == 0 and brunchDone==False:
    brunchDone = True
    for name in restaurantNames:
        print("The following have been assigned to " + str(name) + ":")
        for x in assignmentDict[name]:
            print(str(x) + '\n')

if dinnerDone == True and brunchDone == True:
    print("all these motherfuckers gonna eat")
else:
    print("impossible to fairly assign based on chosen preferences.")
