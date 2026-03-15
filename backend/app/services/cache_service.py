import json
import logging
from typing import Any
import redis
from app.core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.enabled = False
        self.redis_client: Any | None = None
        
        if settings.redis_url:
            try:
                self.redis_client = redis.from_url(
                    settings.redis_url, 
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                # Test connection
                self.redis_client.ping()
                self.enabled = True
                logger.info("✅ Redis cache initialized successfully.")
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed: {e}. Caching will be disabled.")

    def get(self, key: str) -> Any | None:
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Error fetching from cache: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        if not self.enabled or not self.redis_client:
            return
        
        try:
            self.redis_client.set(
                key, 
                json.dumps(value), 
                ex=ttl
            )
        except Exception as e:
            logger.error(f"Error setting cache: {e}")

    def delete(self, key: str):
        if not self.enabled or not self.redis_client:
            return
        
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")

    def clear_all(self):
        if not self.enabled or not self.redis_client:
            return
        
        try:
            self.redis_client.flushdb()
        except Exception as e:
            logger.error(f"Error flushing cache: {e}")

cache = CacheService()