import json

with open('/Volumes/Seagate/good_reviews_v2.json') as f:
    reviews = [json.loads(line) for line in f]
print ('reviews loaded', len(reviews))
with open('/Volumes/Seagate/dataset/business.json') as f:
    business_data = [json.loads(line) for line in f]
print ('business loaded')
with open('/Volumes/Seagate/dataset/user.json') as f:
    user_data = [json.loads(line) for line in f]
print ('user loaded')

reviews = reviews[0]
print ('length of reviews', len(reviews))
sorted_reviews = sorted(reviews, key = lambda x: x['user_id'])






