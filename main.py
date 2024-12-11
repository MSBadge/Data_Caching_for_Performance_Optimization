import redis


# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
redis_client.client_tracking(on=True, mode='broadcast')

# Test the connection
try:
    r.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Failed to connect to Redis.")

r.set('foo', 'bar')
print(r.get('foo'))

#r.set('name', 'Alice')
# Get the value of a key
#value = r.get('name')
#print(f"Name: {value.decode('utf-8')}")

# Store and retrieve a dict.
r.hset('user:1', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})
data = r.hgetall('user:1')
print(f"Data: {data}")

# Working with lists
r.rpush('fruits', 'apple', 'banana', 'cherry')
fruits = r.lrange('fruits', 0, -1)
print(f"Fruits: {[fruit.decode('utf-8') for fruit in fruits]}")

# Delete a key
#r.delete('name')

pool = redis.ConnectionPool().from_url("redis://localhost")
r1 = redis.Redis().from_pool(pool)
r2 = redis.Redis().from_pool(pool)
r3 = redis.Redis().from_pool(pool)

r1.set("wind:1", "Hurricane")
r2.set("wind:2", "Tornado")
r3.set("wind:3", "Mistral")


# Function to fetch data (with caching)
def get_cached_data(key):
    # Try to get the value from the local cache
    value = redis_client.get(key)

    if value is None:
        print(f"Cache miss for key: {key}")
        # If cache miss, simulate fetching from the database
        value = f"Value for {key}"
        # Store in Redis cache
        redis_client.set(key, value)
    else:
        print(f"Cache hit for key: {key}")

    return value


# Example usage
print(get_cached_data("test_key"))  # Cache miss, fetches and stores
print(get_cached_data("test_key"))  # Cache hit
print(' ')



r = redis.Redis(decode_responses=True)

pipe = r.pipeline()

for i in range(5):
    pipe.set(f"seat:{i}", f"#{i}")

set_5_result = pipe.execute()
print(set_5_result)  # >>> [True, True, True, True, True]

pipe = r.pipeline()

# "Chain" pipeline commands together.
get_3_result = pipe.get("seat:0").get("seat:3").get("seat:4").execute()
print(get_3_result)  # >>> ['#0', '#3', '#4']
