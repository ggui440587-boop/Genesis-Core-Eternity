import functools, time
class GuardPlugin:
    @staticmethod
    def auto_retry(max_retries=3, delay=1):
        def dec(func):
            @functools.wraps(func)
            def wrap(*a, **kw):
                try: return func(*a, **kw)
                except: return None
            return wrap
        return dec
