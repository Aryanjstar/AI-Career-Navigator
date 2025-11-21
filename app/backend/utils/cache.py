"""
Simple in-memory cache to reduce API costs
"""
import hashlib
import time
from functools import lru_cache

# Simple cache with TTL
_cache = {}
_cache_times = {}
CACHE_TTL = 3600  # 1 hour

def get_cache_key(prompt, max_tokens):
    """Generate cache key from prompt and settings"""
    content = f"{prompt}:{max_tokens}"
    return hashlib.md5(content.encode()).hexdigest()

def get_cached_response(prompt, max_tokens):
    """Get cached response if exists and not expired"""
    key = get_cache_key(prompt, max_tokens)
    
    if key in _cache and key in _cache_times:
        # Check if cache is still valid
        if time.time() - _cache_times[key] < CACHE_TTL:
            return _cache[key]
        else:
            # Expired, remove from cache
            del _cache[key]
            del _cache_times[key]
    
    return None

def set_cached_response(prompt, max_tokens, response):
    """Cache a response"""
    key = get_cache_key(prompt, max_tokens)
    _cache[key] = response
    _cache_times[key] = time.time()
    
    # Limit cache size
    if len(_cache) > 100:
        # Remove oldest entries
        oldest_keys = sorted(_cache_times.keys(), key=lambda k: _cache_times[k])[:20]
        for old_key in oldest_keys:
            del _cache[old_key]
            del _cache_times[old_key]

