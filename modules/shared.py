def get_environment_value(key):
    import os
    value = os.environ.get(key)
    if not value:
        raise Exception(f"{key} no se encontrĂ³ como variable de ambiente")
    return value