'''

STEPS
1) Divide data into four pieces
2) Calculate p_user (will get list of 4 dictionaries)
3) Join 4 dictoinaries into one
4) Calculate q_item (will get list of )

MAP takes a list of restaurants
Automaticlly divides them up into processes
Updates the other vector set

'''


import random
q_item = {}
p_user = {}
#just random
for r in all_restaurants:
    q_item[r] = [randrange(-10,10)/10 for _ in range(4)]
for u in all_users:
    p_user[u] = [randrange(-10,10)/10 for _ in range(4)]

def init_vectors(data):
    vectors = {}
    for c in data:
        for item in c:
            vectors[item] = [randrange(-10,10)/10 for _ in range(4)]


def calculate_sum_user(tuning_vector, user):
    user_vector = tuning_vector
    uv_mag = np.linalg.norm(user_vector)
    summation = 0
    for restaurant in ratings_by_user[user]:
        item_vector = q_item[restaurant]
        rv_mag = np.linalg.norm(item_vector)
        term = np.dot(user_vector, item_vector) 
        user_dev = user_deviations[user]
        item_dev = restaurant_deviations[restaurant]
        error = (ratings_by_user[user][restaurant] - review_g_average - term - user_dev - item_dev) ** 2 
        + LAMBDA * (uv_mag **2 + rv_mag ** 2 + user_dev ** 2 + item_dev ** 2)
        summation += error
    return summation

def minimize_single_user(user):
    tuning_sums = []
    for tuning_vector in tuning_vectors:
        tuning_sum = calculate_sum_user(tuning_vector, user)
        tuning_sums.append((tuning_vector, tuning_sum))
    best = (min(tuning_sums, key = lambda x: x[1])[0])
    difference = abs(best[0] - p_user[user][0]) + abs(best[1] - p_user[user][1])
    + abs(best[2] - p_user[user][2]) + abs(best[3] - p_user[user][3])
    p_user[user] = best

def minimize_user_vectors():
    pool = mp.Pool(processes=4)
    results = pool.map(minimize_single_user, all_users, 4)

def calculate_sum_item(tuning_vector, item):
    item_vector = tuning_vector
    rv_mag = np.linalg.norm(item_vector)
    summation = 0
    for user in ratings_by_restaurant[item]:
        user_vector = p_user[user]
        uv_mag = np.linalg.norm(user_vector)
        term = np.dot(item_vector, user_vector) 
        user_dev = user_deviations[user]
        item_dev = restaurant_deviations[item]
        error = (ratings_by_restaurant[item][user] - review_g_average - user_dev - item_dev - term) ** 2 
        + LAMBDA * (uv_mag **2 + rv_mag ** 2 + user_dev ** 2 + item_dev ** 2)
        summation += error
    return summation

def minimize_single_item(item):   
    tuning_sums = []
    for tuning_vector in tuning_vectors:
        tuning_sum = calculate_sum_item(tuning_vector, item)
        tuning_sums.append((tuning_vector, tuning_sum))
    best = (min(tuning_sums, key = lambda x: x[1])[0])
    difference = abs(best[0] - q_item[item][0]) + abs(best[1] - q_item[item][1]) 
    + abs(best[2] - q_item[item][2]) + abs(best[3] - q_item[item][3])
    q_item[item] = best

def minimize_item_vectors():
    pool = mp.Pool(processes=4)
    results = pool.map(minimize_single_item, all_restaurants, 4)


    print ('HELLO')
    print ('minimizing user vectors')
    conv = minimize_user_vectors()
    print (conv)
    #whil vectors have not converged
    while conv > 10: 
        for _ in range(1000):
            print ('minimizing item vectors')
            conv = minimize_item_vectors()
            print (conv)
            print ('minimizing user vectors')
            conv = minimize_user_vectors()
            print (conv)
                 


# In[92]:

ALS_4(q_item, p_user, ratings_by_restaurant_train, ratings_by_user_train)
