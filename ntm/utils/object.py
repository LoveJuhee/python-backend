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

    @staticmethod
    def is_null_or_empty(item):
        if item is None:
            return True
        try:
            if len(item) > 0:
                return False
        except:
            return True
        return True
