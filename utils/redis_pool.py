import redis


class RedisConfig:
    HOST = '192.168.2.74'
    PORT = 9736
    PASSWORD = '1e3s5l'


class RedisModel:
    def __init__(self):
        if not hasattr(RedisModel, 'pool'):
            RedisModel.create_pool()

        self._connection = redis.Redis(connection_pool=RedisModel.pool, decode_responses=True)

    @staticmethod
    def create_pool():
        RedisModel.pool = redis.ConnectionPool(
            host=RedisConfig.HOST,
            port=RedisConfig.PORT,
            password=RedisConfig.PASSWORD,
            decode_responses=True
        )

    def set_data(self, key, value):
        """ set data with (key, value)
        """
        return self._connection.set(key, value)

    def get_data(self, key):
        """ get data by key
        """
        return self._connection.get(key)

    def del_data(self, key):
        """ delete cache by key
        """
        return self._connection.delete(key)

    def get_hash_data(self, key, hkey):
        """
        获取哈希表指定键的值
        :param key:
        :param hkey:
        :return:
        """

        return self._connection.hget(key, hkey)

    def get_hash_all_data(self, key):
        """
        获取哈希表全部键和值
        :param key: redis键
        :return: 字典
        """

        return self._connection.hgetall(key)

    def set_hash_data(self, key, hkey, hval):
        """
        设置哈希表指定键的值，如果key不存在则会自动创建
        :param key: redis键
        :param hkey: 字典键
        :param hval: 字典值
        :return:
        """

        return self._connection.hset(key, hkey, hval)
