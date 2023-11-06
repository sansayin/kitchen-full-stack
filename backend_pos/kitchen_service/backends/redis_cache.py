from django_redis.cache import RedisCache


class CustomRedisCache(RedisCache):
    def __init__(self, server, params):
        # Set the charset and errors options
        params["charset"] = "utf-8"
        params["errors"] = "strict"
        super().__init__(server, params)
