
                     

def ALS_4(q_item, p_user, ratings_by_restaurant, ratings_by_user, LAMBDA = 10):
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

    def minimize_user_vectors_CV():
        convergence = 0
        for user in ratings_by_user:
            tuning_sums = []
            for tuning_vector in tuning_vectors:
                tuning_sum = calculate_sum_user(tuning_vector, user)
                tuning_sums.append((tuning_vector, tuning_sum))
            best = (min(tuning_sums, key = lambda x: x[1])[0])
            difference = abs(best[0] - p_user[user][0]) + abs(best[1] - p_user[user][1])
            + abs(best[2] - p_user[user][2]) + abs(best[3] - p_user[user][3])
            p_user[user] = best
            convergence += difference
        return convergence

    def calculate_sum_item_CV(tuning_vector, item):
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


    def minimize_item_vectors():
        convergence = 0
        for item in ratings_by_restaurant:
            tuning_sums = []
            for tuning_vector in tuning_vectors:
                tuning_sum = calculate_sum_item(tuning_vector, item)
                tuning_sums.append((tuning_vector, tuning_sum))
            best = (min(tuning_sums, key = lambda x: x[1])[0])
            difference = abs(best[0] - q_item[item][0]) + abs(best[1] - q_item[item][1]) 
            + abs(best[2] - q_item[item][2]) + abs(best[3] - q_item[item][3])
            q_item[item] = best
            convergence += difference
        return convergence

    
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
                 