"""Tests for KV Cache Evictor."""
import unittest
from kv_cache_semantic_evictor.core import KVCacheSemanticEvictor

class TestKVCacheSemanticEvictor(unittest.TestCase):
    def test_eviction_preserves_sink_and_high_attention(self):
        e = KVCacheSemanticEvictor(max_capacity=4, sink_size=2)
        e.append(101, 0.5) # sink
        e.append(102, 0.5) # sink
        e.append(103, 0.1) # low
        e.append(104, 0.2) # low
        e.append(105, 0.9) # high! triggers eviction
        
        tokens = e.get_token_ids()
        self.assertEqual(len(tokens), 4)
        self.assertIn(101, tokens) # sink preserved
        self.assertIn(102, tokens) # sink preserved
        self.assertIn(105, tokens) # high attention preserved
