import redis

redis_url = "redis://localhost:6379/0"
redis = redis.Redis.from_url(redis_url)