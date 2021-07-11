import redis as redis_client

# redis = redis_client.Redis(host='127.0.0.1', port=6380, db=0)
redis = redis_client.Redis(host='redis_db', port=6379, db=0)