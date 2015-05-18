def method_cache(seconds=0):
    """
    A `seconds` value of `0` means that we will not memcache it.

    If a result is cached on instance, return that first.  If that fails, check
    memcached. If all else fails, hit the db and cache on instance and in
     memcache.

    ** NOTE: Methods that return None are always "recached".
    """

    from hashlib import sha224
    from django.core.cache import cache

    def inner_cache(method):

        def x(instance, *args, **kwargs):
            key = sha224(str(method.__module__).encode()
                         + str(method.__name__).encode()
                         + str(instance.id).encode()
                         + str(args).encode()
                         + str(kwargs).encode()).hexdigest()

            if hasattr(instance, key):
                # has on class cache, return that
                result = getattr(instance, key)
            else:
                result = cache.get(key)

                if result is None:
                    # all caches failed, call the actual method
                    result = method(instance, *args, **kwargs)

                    # save to memcache and class attr
                    if seconds and isinstance(seconds, int):
                        cache.set(key, result, seconds)
                    setattr(instance, key, result)

            return result

        return x

    return inner_cache
