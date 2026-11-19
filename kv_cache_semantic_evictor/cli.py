"""CLI for KV Cache Evictor."""
import argparse
from .core import KVCacheSemanticEvictor

def main():
    parser = argparse.ArgumentParser(description="KV Cache Semantic Evictor CLI")
    parser.add_argument("--demo", action="store_true", help="Run evictor demo")
    args = parser.parse_args()

    evictor = KVCacheSemanticEvictor(max_capacity=8, sink_size=2)
    for i in range(15):
        score = 0.9 if i in (0, 1, 10, 14) else 0.1
        evictor.append(i, score)
    print(f"Retained tokens after eviction: {evictor.get_token_ids()}")

if __name__ == "__main__":
    main()
