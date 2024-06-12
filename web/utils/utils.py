from os import environ


def get_env_variable(variable):
    if variable not in environ:
        raise RuntimeError(
            f"You are not specified variable {variable} in .env file in project root. Please do this and rerun docker compose up"
        )
    return environ[variable]
