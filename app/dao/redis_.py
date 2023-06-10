import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)
