#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquerystring import parse

from collections import Counter
from pprint import pprint
import timeit
from urlparse import parse_qsl


def bench_urlparse():
    parse_qsl("id=1")

def bench():
    parse("id=1")

if __name__ == '__main__':

    c = Counter()

    t = timeit.Timer(stmt='bench_urlparse()', setup='from __main__ import bench_urlparse')
    c['parse_qsl simple'] = t.timeit(number=1000) * 100

    t = timeit.Timer(stmt='bench()', setup='from __main__ import bench')
    c['pyquerystring simple'] = t.timeit(number=1000) * 100

    pprint(c)
