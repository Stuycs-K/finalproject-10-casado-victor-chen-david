import math
import time

for i in range(3):
    current_unix_time = time.time()
    print(math.floor(current_unix_time/30))

    secret_key = 0xAAAA0000AAAA
    print(secret_key)
    time.sleep(30)
