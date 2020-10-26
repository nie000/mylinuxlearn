import redis
pool = redis.ConnectionPool(host='localhost', port=6379,db=1)
red = redis.Redis(connection_pool=pool)
red.set('key1', 'value1')
red.set('key2', 'value2')