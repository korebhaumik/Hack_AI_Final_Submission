import redis

# locally running redis
redis_url = "redis://localhost:6379/0"
redis_client = redis.Redis.from_url(redis_url)
