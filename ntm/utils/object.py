import pprint
from io import StringIO


class ObjectUtil():
    """
    객체에 대한 유틸
    """

    @staticmethod
    def get_value(item, indent=1, width=80, depth=None):
        """
        item: 상세정보를 나타낼 객체
        """
        s = StringIO()
        pprint.pprint(item, s, indent, width, depth)
        return s.getvalue()

    def is_null_or_empty(*args):
        if len(args) == 0:
            return True
        try:
            for item in args:
                if item is None:
                    return True
                elif len(item) == 0:
                    return True
        except:
            return True
        return False
