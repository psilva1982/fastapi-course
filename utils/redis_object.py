from utils.constants import REDIS_URL, TESTING, TEST_REDIS_URL
import aioredis

redis = None

async def check_test_redis():
    global redis
    
    if TESTING:
        redis = await aioredis.create_redis_pool(TEST_REDIS_URL)