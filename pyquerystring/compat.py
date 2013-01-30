# -*- coding: utf-8 -*-
# from requests:
# https://github.com/kennethreitz/requests/blob/master/requests/compat.py

import sys
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

if is_py2:
    from urlparse import parse_qsl
elif is_py3:
    from urllib.parse import parse_qsl
