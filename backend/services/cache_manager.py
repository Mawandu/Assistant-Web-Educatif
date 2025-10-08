# backend/services/cache_manager.py
import redis
import json
import os

class CacheManager:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.client = redis.from_url(redis_url)
        print("Connecté au cache Redis.")

    def get(self, key: str):
        """Récupère une valeur depuis le cache."""
        cached_value = self.client.get(key)
        if cached_value:
            return json.loads(cached_value)
        return None

    def set(self, key: str, value: dict, ttl: int = 3600):
        """Stocke une valeur dans le cache avec une durée de vie (ttl) en secondes."""
        self.client.setex(key, ttl, json.dumps(value))