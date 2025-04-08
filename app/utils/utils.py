import random
import string
from datetime import datetime, timezone


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_current_time() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    print(generate_id())
    print(get_current_time())