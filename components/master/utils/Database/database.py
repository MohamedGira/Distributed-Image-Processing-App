import redis
class RedisDatabase:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = redis.Redis(host=host, port=port, db=0,decode_responses= True)
    
    def save_dict(self, key, value):
        self.connection.hset(key,mapping=value)
    
    def get_dict(self, key):
        return self.connection.hgetall(key)
    
    def update_dict(self, key, value):
        self.connection.hmset(key, value)