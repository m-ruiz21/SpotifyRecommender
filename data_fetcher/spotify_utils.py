import tekore as tk
import time

def castToInt(var) -> int:
    if var is None:
        return 0
    else:
        return int(var)

def runWithRetry(fun, *args, **kwargs): 
    retries = 0 
    while True: 
        try:
            return fun(*args, **kwargs)
        except tk.TooManyRequests as e:
            retry_after = e.response.headers.get('Retry-After')
            print(f"ERROR: failed to run function{fun.__name__}: too many requests. retrying in {retry_after} seconds...")
            time.sleep(retry_after)
            pass
