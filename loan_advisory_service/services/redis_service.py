from redis.asyncio import ConnectionPool, Redis
from loan_advisory_service.main.config import RedisConfig


def get_redis_pool(config: RedisConfig) -> ConnectionPool:
    return ConnectionPool(
        host=config.host,
        port=config.port,
        password=config.password,
        decode_responses=True,
    )


def get_redis_client(pool: ConnectionPool) -> Redis:
    return Redis.from_pool(pool)



