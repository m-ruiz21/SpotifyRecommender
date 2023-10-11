import tekore as tk
import time

def runWithRetry(fun, *args, **kwargs): 
    retries = 0 
    while True: 
        try:
            return fun(*args, **kwargs)
        except tk.TooManyRequests:
            retries += 1
            print(f"ERROR: failed to run function {fun}, retrying in {30 * retries} seconds...")
            time.sleep(30 * retries)
            pass
