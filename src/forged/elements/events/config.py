_backend_config = {
    "action": "pydispatcher",
    "activity": "rxpy",
}

def set_backend(action=None, activity=None):
    if action:
        _backend_config["action"] = action
    if activity:
        _backend_config["activity"] = activity

def get_backend(which):
    return _backend_config[which]