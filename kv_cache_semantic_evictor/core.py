"""Core KV Cache Semantic Evictor."""
from typing import List, Dict, Optional, Tuple
import math

class CacheTokenEntry:
    def __init__(self, token_id: int, attention_score: float, is_sink: bool = False):
        self.token_id = token_id
        self.attention_score = attention_score
        self.is_sink = is_sink

class KVCacheSemanticEvictor:
    def __init__(self, max_capacity: int = 1000, sink_size: int = 4):
        self.max_capacity = max_capacity
        self.sink_size = sink_size
        self.cache: List[CacheTokenEntry] = []

    def append(self, token_id: int, attention_score: float):
        is_sink = len(self.cache) < self.sink_size
        self.cache.append(CacheTokenEntry(token_id, attention_score, is_sink=is_sink))
        if len(self.cache) > self.max_capacity:
            self._evict()

    def _evict(self):
        sink_tokens = self.cache[:self.sink_size]
        dynamic_tokens = self.cache[self.sink_size:]
        
        # Sort dynamic tokens by attention score descending and retain top budget
        keep_count = self.max_capacity - self.sink_size
        dynamic_tokens.sort(key=lambda t: t.attention_score, reverse=True)
        retained = dynamic_tokens[:keep_count]
        
        self.cache = sink_tokens + retained

    def get_token_ids(self) -> List[int]:
        return [t.token_id for t in self.cache]
