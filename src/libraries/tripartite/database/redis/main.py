import redis

r = redis.cluster.RedisCluster(
    host="localhost",
    port=6371,
    password="120e204105de1345fda9f27911c02f66",
)

r.set("foo", "bar")
r.get("foo")
