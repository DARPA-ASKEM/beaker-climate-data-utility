from elwood import elwood

_result = {}

functions = [x for x in dir(elwood) if not x.startswith('__')]

for attr_name in functions:
    attr = getattr(elwood, attr_name)
    if hasattr(attr, '__doc__'):
        _result[attr_name] = attr.__doc__

_result
