import redis.asyncio as redis


class RedisManager:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.redis: redis.Redis | None = None

    async def connect(self):
        self.redis = redis.Redis(host=self.host, port=self.port, decode_responses=True)

        # connection check
        await self.redis.ping()

    def _redis_is_connected(self):
        if not self.redis:
            raise RuntimeError("Redis is not connected")

    async def get(self, key: str):
        self._redis_is_connected()
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int | None = None):
        self._redis_is_connected()
        await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        self._redis_is_connected()
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
