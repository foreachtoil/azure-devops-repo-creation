def get_environment_value(key):
    import os
    value = os.environ.get(key)
    if not value:
        raise Exception(f"{key} no se encontró como variable de ambiente")
    return value