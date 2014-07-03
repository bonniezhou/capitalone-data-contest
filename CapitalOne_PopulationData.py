#Capital One - Population Data Challenge

import csv

#------------------------------------------
#growth_rate: int, int -> float

#growth_rate() takes 2 integer parameters popn1 and popn2, and produces the
#growth rate between popn1 and popn2 as a float

def growth_rate(popn1, popn2):
    if popn1 == 0:
        return 0
    else:
        return popn2/float(popn1) - 1

#------------------------------------------
#city_popn: csv_file -> (listof (listof str int int))
    
#city_popn() takes a population csv file and produces a list of lists of length 3,
#where the 1st element is the city name as a string, the 2nd element is the
#population in 2010 as an integer, and the 3rd element is the population in 2012
#as an integer
    
def city_popn(popfile):
    city_popn = []
    row_count = 0
    with open(popfile, 'rU') as f:
        reader = csv.reader(f)

        for row in reader:
            if row_count == 0:
                row_count = 1
                continue
            city = row[0]
            pop2010 = int(row[1])
            pop2012 = int(row[3])
            city_row = [city, pop2010, pop2012]
            city_popn.append(city_row)

    return city_popn

#------------------------------------------
#list_states: (listof (listof str int int)) -> (listof str)

#list_states() takes a list produced by city_popn() and produces a list of the
#names of all states as a string

def list_states(city_popn):
    states = []  
    for city_row in city_popn:
        state = city_row[0].split(',')[1]
        if state not in states: #search more efficiently
            states.append(state)      
    return states

#------------------------------------------
#state_popn: (listof (listof str)), (listof (listof str int int)) -> (listof (listof str int int))

#state_popn() takes a list produced by list_states() and a list produced by
#city_popn() and produces a list of lists similar to that produced by
#city_popn(), but where the 1st element of the inner list are names of states

def state_popn(states_list, city_popn):
    state_popn = []
    for state in states_list:
        state_row = [state, 0, 0]
        state_popn.append(state_row)
        
    for city_row in city_popn:
        state = city_row[0].split(',')[1]
        for state_row in state_popn: #make more efficient
            if state_row[0] == state:
                state_row[1] = state_row[1] + city_row[1]
                state_row[2] = state_row[2] + city_row[2]
                
    return state_popn

#------------------------------------------
#popn_dict: (listof (listof str int int)), bool -> dict

#popn_dict() takes a list of lists produced by either state_popn() or
#city_popn() and a boolean parameter representing whether there is a
#minimum population of 50,000, and produces a dictionary where the
#key is the city/state and the value is the population growth rate
#between 2010 and 2012

def popn_dict(popn_list, over_5k):
    popn_dict = {}
    for row in popn_list:
        pop2010 = row[1]
        pop2012 = row[2]

        if over_5k:
            if pop2010 > 50000:
                growth = growth_rate(pop2010, pop2012)
                popn_dict[row[0]] = growth
        else:
            growth = growth_rate(pop2010, pop2012)
            popn_dict[row[0]] = growth

    return popn_dict

#------------------------------------------
#best: dict -> (tupleof (listof str) (listof str))

#best() takes a dictionary produced by popn_dict() and produces a
#2-tuple where the 1st element is a list of the 5 cities/states
#with the highest growth rate (to target), and the 2nd element is
#a list of the 5 cities/states with the lowest growth rate (to avoid)
#side effect: deletes from the dictionary all 10 cities/states in the
#tuple produced

def best(popn_dict):
    count = 0
    highest_growth = []
    lowest_growth = []
    
    while count < 5:
        highest_growth.append(max(popn_dict))
        lowest_growth.append(min(popn_dict))
        del popn_dict[max(popn_dict)], popn_dict[min(popn_dict)]
        count = count + 1

    return (highest_growth, lowest_growth)


#------------------------------------------
#------------------------------------------


#EXECUTABLE SCRIPT

city = city_popn('Metropolitan_Populations__2010-2012.csv')
states = state_popn(list_states(city), city)
city_dict = popn_dict(city, 1)
state_dict = popn_dict(states, 0)

#Top five cities to target based on highest population growth between 2010-2012
cities_to_target = best(city_dict.copy())[0]

#Top five cities to avoid based on the most shrinking population between 2010-2012
cities_to_avoid = best(city_dict.copy())[1]

#Top five states with highest cumulative growth between 2010-2012
states_to_target = best(state_dict.copy())[0]

