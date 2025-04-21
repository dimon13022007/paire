from cachetools import TTLCache

user_view_count = TTLCache(maxsize=1000, ttl=3600)
image_cache = TTLCache(maxsize=100, ttl=600)

