from datetime import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            now = datetime.now()
            
            try:
                result = old_function(*args, **kwargs)
            except Exception as e:
                result = f"Ошибка: {e}"
                raise

            log_entry = (
                f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Функция: '{old_function.__name__}', "
                f"Аргументы: args={args}, kwargs={kwargs}, "
                f"Результат: {type(result).__name__} (длина: {len(str(result))} симв.)\n"
            )
            
            with open(path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return result
        return new_function
    return __logger