import types
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


@logger(file_path="test-log.txt")
def flat_generator(list_of_lists):
    for i in [j for i in list_of_lists for j in i]:
        yield i


def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
