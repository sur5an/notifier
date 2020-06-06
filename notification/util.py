import os


class Util:
    @staticmethod
    def check_env_variable(variables):
        for v in variables:
            if v not in os.environ:
                return False
            if os.environ[v] is None:
                return False
            if len(str(os.environ[v]).strip()) == 0:
                return False
        return True

    @staticmethod
    def get_env_variable(variable, default):
        resp = default
        if len(str(os.environ[variable]).strip()) > 0:
            resp = str(os.environ[variable]).strip()
        return resp
