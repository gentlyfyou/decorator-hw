from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        now = datetime.now()
        result = old_function(*args, **kwargs)
        
        log_entry = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Функция: {old_function.__name__}, args={args}, kwargs={kwargs}, результат={result}\n"
        
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        return result
    return new_function


def logger_parametrized(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            now = datetime.now()
            result = old_function(*args, **kwargs)
            
            log_entry = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Функция: {old_function.__name__}, args={args}, kwargs={kwargs}, результат={result}\n"
            
            with open(path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return result
        return new_function
    return __logger.gitignore  