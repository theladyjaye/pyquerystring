
# Fancy query string parsing & application/x-www-form-urlencoded parsing
#
# Copyright 2011 Adam Venturella
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl


ARRAY = "ARRAY"
OBJECT = "OBJECT"
KEY = "KEY"
VALUE = "VALUE"
DLE = "\x10"

#Token = namedtuple('Token', 'type value')


class QueryStringParser(object):

    def __init__(self, qs):
        self.result = {}
        pairs = parse_qsl(qs)

        # we don't know how a user might pass in array indexs
        # so sort the keys first to ensure it's in a proper order
        sorted_pairs = sorted(pairs, key=lambda pair: pair[0])

        #map(self.process, sorted_pairs)
        [self.process(x) for x in sorted_pairs]

    def process(self, pair):
        key = pair[0]
        value = pair[1]

        def parse(value):
            receiver = self.protocol_receiver()
            next(receiver)
            protocol = self.protocol(target=receiver)
            next(protocol)
            for char in key:
                protocol.send(char)
            protocol.send(DLE)

            receiver.send((VALUE, value))

        # faster than invoking a regex
        # do we even need to parse anything?
        # if one test for a token passes, it all
        # must be parsed, return immediately because
        # we don't care if the other tests passes,
        # it's already been parsed.
        try:
            key.index("[")
            parse(value)
            return
        except ValueError:
            pass

        try:
            key.index(".")
            parse(value)
            return
        except ValueError:
            pass

        self.result[key] = value

    def protocol_receiver(self):
        ref = self.result

        while 1:
            token = (yield)
            type, key = token

            if type == ARRAY:
                if key not in ref:
                    try:
                        ref[key] = []
                    except TypeError:
                        continue
                ref = ref[key]

            elif type == OBJECT:
                if key not in ref:
                    ref[key] = {}
                ref = ref[key]

            elif type == KEY:
                try:
                    ref = ref[key]
                    token = (yield)
                # TypeError is for pet[]=lucy&pet[]=ollie
                # if the array key is empty a type error will be raised
                except (IndexError, KeyError, TypeError):
                    # the index didn't exist
                    # so we look ahead to see what we are setting
                    # there is not a next token
                    # set the values
                    n_type, n_key = (yield)

                    if n_type == ARRAY:
                        ref.append([])
                        ref = ref[key]

                    elif n_type == OBJECT:
                        try:
                            ref[key] = {}
                        except IndexError:
                            ref.append({})

                        ref = ref[key]

                    # always arrays?
                    elif n_type == VALUE:
                        try:
                            ref.append(n_key)
                        except AttributeError:
                            ref[key] = n_key

    def protocol(self, array='[',
                       obj='.',
                       key=']',
                       dle='\x10',
                       target=None):
        while 1:
            byte = (yield)
            buf = ''
            while 1:
                if byte == array:
                    token = (ARRAY, buf)
                    target.send(token)
                    buf = None
                    break

                elif byte == obj:
                    token = (OBJECT, buf)
                    target.send(token)
                    buf = None
                    break

                elif byte == key:
                    try:
                        token = (KEY, int(buf))
                        target.send(token)
                        buf = None
                    except ValueError:
                        token = (KEY, None)
                        target.send(token)
                    break

                elif byte == dle:
                    break

                else:
                    buf += byte

                byte = (yield)

            if buf:
                target.send((KEY, buf))
