Build a tiny data utility that computes the average of numbers and caches the result in Redis.

Requirements:
1) Ensure a Redis server is running locally and reachable at 127.0.0.1:6379
   - You may start it in the background (daemonized) if needed
2) Create a Python script at /app/cache_stats.py that:
   - Reads integers line-by-line from /app/numbers.txt
   - Computes the arithmetic average and formats it with exactly two decimal places
   - Writes the formatted average to /app/result.txt (e.g., "7.50")
   - Stores the same formatted average into Redis under the key "stats:avg"
   - The Redis key must have a TTL (time-to-live) of 300 seconds
   - The script must be re-runnable: when /app/numbers.txt changes and the script is run again, it should recompute, rewrite /app/result.txt, and update the Redis key and its TTL
3) After implementing the script, run it once so that:
   - /app/result.txt exists with the correct average for the current /app/numbers.txt
   - The Redis key "stats:avg" is set and has a TTL (<= 300 seconds)

Provided:
- A starter /app/numbers.txt file will already be present in the container

What we will test:
- Redis is reachable (PING)
- /app/cache_stats.py exists and is runnable
- /app/result.txt matches the expected average (two decimals)
- Redis key "stats:avg" exists with the correct value and a TTL <= 300
- Re-running /app/cache_stats.py after modifying /app/numbers.txt recomputes and updates both the file and Redis

Hints:
- You can use redis-cli to interact with Redis (e.g., SETEX for key with TTL)
- Make sure your script handles whitespace and empty lines gracefully