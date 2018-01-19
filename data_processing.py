from data import sorted_reviews as reviews
from data import business_data, user_data
import random

train_set = []
valid_set = []
test_set = []
for i,x in enumerate(reviews):
    short = {k: x[k] for k in ['business_id', 'stars', 'user_id']}
    if i % 3 == 0:
        train_set.append(short)
    elif i % 3 == 1:
        valid_set.append(short)  
    else:
        test_set.append(short)



all_users = set([x['user_id'] for x in reviews])
all_restaurants = set([x['business_id'] for x in reviews])
print len(train_set)

user_dict = {x['user_id']: x['average_stars'] for x in user_data}
restaurant_dict = {x['business_id']: x['stars'] for x in business_data}
user_ratings = {x: user_dict[x] for x in all_users}
restaurant_ratings = {x: restaurant_dict[x] for x in all_restaurants}

user_g_average = np.mean(list(user_ratings.values()))
restaurant_g_average = np.mean(list(restaurant_ratings.values()))


user_deviations = {x: user_ratings[x] - user_g_average for x in user_ratings}
restaurant_deviations = {x: restaurant_ratings[x] - restaurant_g_average for x in restaurant_ratings}
review_g_average = np.mean(train_df['stars'])


ratings_by_restaurant_train = {}
ratings_by_user_train = {}

for i in range(len(train_df)):
    row = train_df.iloc[i]
    bus_id = row[0]
    stars = row[1]
    user_id = row[2]
    if bus_id not in ratings_by_restaurant_train:
        ratings_by_restaurant_train[bus_id] = {user_id : stars}
    else:
        ratings_by_restaurant_train[bus_id][user_id] = stars
        
    if user_id not in ratings_by_user_train:
        ratings_by_user_train[user_id] = {bus_id : stars}
    else:
        ratings_by_user_train[user_id][bus_id] = stars

import random
q_item = {}
p_user = {}
#just random
for r in ratings_by_restaurant_train:
    q_item[r] = [randrange(-10,10)/10 for _ in range(4)]
for u in ratings_by_user_train:
    p_user[u] = [randrange(-10,10)/10 for _ in range(4)]


# In[64]:

tuning_vectors = []
tuning_values = [x/10 for x in range(-9, 9)]
for a in tuning_values:
    for b in tuning_values:
        for c in tuning_values:
            for d in tuning_values:
                tuning_vectors.append([a, b, c, d])

print (tuning_vectors, 'tuning_vectors')







    
'''