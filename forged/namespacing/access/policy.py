class ResolutionPolicy:
    def __init__(self):
        self.rules = []

    def add_rule(self, match_fn, resolve_fn):
        """
        match_fn(context) → bool
        resolve_fn(path, context) → value
        """
        self.rules.append((match_fn, resolve_fn))

    def resolve(self, path: str, context: dict, default_resolver):
        for match_fn, resolve_fn in self.rules:
            if match_fn(context):
                return resolve_fn(path, context)
        return default_resolver(path, context)
