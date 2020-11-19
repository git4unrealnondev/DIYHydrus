from ratelimiter import RateLimiter
def limit(until):
    print("Rate Limited for ", until)
rate_limiter = RateLimiter(max_calls=1, period=5, callback=limit)


for i in range(200):
    with rate_limiter:
        print("Iteration", i)
