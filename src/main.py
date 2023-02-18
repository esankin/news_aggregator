import asyncpg
import redis
from fastapi import FastAPI
from .config import settings
app = FastAPI()

query = """
select pid as process_id, 
       usename as username, 
       datname as database_name, 
       client_addr as client_address, 
       application_name,
       backend_start,
       state,
       state_change
from pg_stat_activity;
"""


@app.get('/health')
async def root():
    conn = await asyncpg.connect(
        f'postgresql://{settings.postgres_user}:{settings.postgres_password}@postgres/news_db',
    )
    result = await conn.fetch(query)
    conn.close()
    redis_conn = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
    )
    redis_conn.set('health', 'checked')
    redis_health = redis_conn.get('health')
    redis_conn.close()
    return {
        'message': 'Hello World',
        'psql': bool(len(result)),
        'redis': bool(redis_health),
    }

