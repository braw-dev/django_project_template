from django.contrib.auth.hashers import Argon2PasswordHasher


class SecureArgon2PasswordHasher(Argon2PasswordHasher):
    # Recommended values from OWASP
    # https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
    time_cost = 2  # 2 iterations
    memory_cost = 20 * 1024  # 20MB
    parallelism = 1  # 1 parallel
