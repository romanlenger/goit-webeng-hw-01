from functools import wraps


def bot_error(func):
    """
    Декоратор для обробки помилок вводу.
    """
    @wraps(func)
    def inner( *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return print("@bot_error : KeyError : Contact not found.")
        except ValueError:
            return print("@bot_error : ValueError : Перевірте кількість та правильність вводу аргументів.")
        except IndexError:
            return print("@bot_error : Index Error")
        except TypeError:
                return print("@bot_error : TypeError")
    return inner


def display_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print(f"@display_error: Перевірте кількість та правильність вводу аргументів.")
            # Можете добавить дополнительную обработку или логирование здесь
    return wrapper