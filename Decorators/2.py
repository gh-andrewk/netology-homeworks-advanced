import os
from datetime import datetime

def logger(_func=None, *, file_path):
    def _wrapeer(func):
        dt = datetime.now()
        func_name = func.__name__
        def new_function(*args, **kwargs):
            with open(file_path, "a", encoding="utf8") as f:
                result = func(*args, **kwargs)
                f.write(f"{dt} - {func_name}, {args=}, {kwargs=}, {result=}\n")
            return result
        return new_function
    if _func is None:
        return _wrapeer
    return _wrapeer(_func)


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(file_path=path)
        def hello_world():
            return 'Hello World'

        @logger(file_path=path)
        def summator(a, b=0):
            return a + b

        @logger(file_path=path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
