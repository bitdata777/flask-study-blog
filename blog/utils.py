def request_to_class(request, *args):

    class SoftDict:

        def __init__(self, user_dict):
            self._user_dict = user_dict
            self._parse()

        def _parse(self):
            for key in self._user_dict.keys():
                value = self._user_dict[key]
                if type(value) == dict:
                    value = SoftDict(value)
                setattr(self, key, value)

        def hasattr(self, *items):
            emptyattrs = str()
            for row, item in len(items):
                if not hasattr(self, item):
                    emptyattrs += item
                    if row + 1 != len(items):
                        emptyattrs += ', '
            if emptyattrs is None:
                return True
            raise AttributeError(emptyattrs)

        #  def __getattribute__(self, item):
        #      try:
        #          return super().__getattribute__(item)
        #      except AttributeError:
        #          raise ValueError(item)

    def is_listtype(value):
        if ',' in value:
            return True
        return False

    def is_dicttype(value):
        values = value.split(',')
        for v in values:
            if '=' not in v:
                return False
        return True

    def make_dict(value):
        tmp = value.split('=')
        return {tmp[0] : tmp[1]}

    def make_dicts(value):
        return dict(query.split('=') for query in value.split(','))

    def make_list(value):
        values = value.split(',')
        value_list = list()
        for v in values:
            if is_dicttype(v):
                value_list.append(make_dict(v))
                continue
            value_list.append(v)
        return value_list

    def exception_keyword(key):
        if key in args:
            return True
        return False

    def get_param_by_request(request):
        if request.method == 'GET':
            return request.args
        return request.form

    params = get_param_by_request(request)
    args_dict = dict()

    for key in params.keys():
        if exception_keyword(key):
            args_dict[key] = params[key]
            continue
        # 인자값이 ',' 으로 구성되어 있으면
        if is_listtype(params[key]):
            if is_dicttype(params[key]):
                args_dict[key] = make_dicts(params[key])
            else:
                args_dict[key] = make_list(params[key])
        elif is_dicttype(params[key]):
            args_dict[key] = make_dict(params[key])
        else:
            args_dict[key] = params.get(key)
    return SoftDict(args_dict)
