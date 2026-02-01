python
import time

def generate_unique_name(base_name: str) -> str:
    return f"{base_name} {int(time.time() * 1000)}"
