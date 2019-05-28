"""
 Created by hanruida on 2019-03-22
"""
import hashlib


class Codecs:
    """
        md5加密
    """
    @staticmethod
    def md5(name):
        new_str = ''
        if isinstance(name, str):
            new_str = name.encode("utf8")
        m = hashlib.md5()
        m.update(new_str)
        return m.hexdigest()
