"""

"""

_default_action_types = [
    'read', 'r',
    'write', 'w',
    'del', 'd',
    'exec', 'e'
]

class ACLRule:
    def __init__(self, action: str, roles: list[str] = None, env: str = None, allow: bool = True):
        self.action = action
        self.roles = roles or []
        self.env = env
        self.allow = allow

    def matches(self, action: str, context: dict) -> bool:
        if self.action != action:
            return False
        if self.env and self.env != context.get("env"):
            return False
        if self.roles and not (any(role in context.get("roles", []))):
            return False
        return True

class ACL:
    """
    Access Control List
    """
    def __init__(self):
        self.rules: list[ACLRule] = []

    def allow(self, action: str, roles=None, env=None):
        self.rules.append(ACLRule(action, roles or [], env, allow=True))

    def deny(self, action: str, roles=None, env=None):
        self.rules.append(ACLRule(action, roles or [], env, allow=False))

    def check(self, action: str, context: dict) -> bool:
        for rule in self.rules:
            if rule.matches(action, context):
                return rule.allow
        return True  # allow if no matching rule
