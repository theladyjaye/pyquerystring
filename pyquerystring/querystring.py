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


class QueryStringToken(object):

    ARRAY = "ARRAY"
    OBJECT = "OBJECT"
    KEY = "KEY"


class QueryStringParser(object):

    def __init__(self, qs):
        self.result = {}
        pairs = parse_qsl(qs)

        # we don't know how a user might pass in array indexs
        # so sort the keys first to ensure it's in a proper order
        sorted_pairs = sorted(pairs, key=lambda pair: pair[0])

        [self.process(x) for x in sorted_pairs]

    def process(self, pair):
        key = pair[0]
        value = pair[1]

        #faster than invoking a regex
        try:
            key.index("[")
            self.parse(key, value)
            return
        except ValueError:
            pass

        try:
            key.index(".")
            self.parse(key, value)
            return
        except ValueError:
            pass

        self.result[key] = value

    def parse(self, key, value):
        ref = self.result
        tokens = self.tokens(key)

        for token in tokens:
            token_type, key = token

            if token_type == QueryStringToken.ARRAY:
                if key not in ref:
                    ref[key] = []
                ref = ref[key]

            elif token_type == QueryStringToken.OBJECT:
                if key not in ref:
                    ref[key] = {}
                ref = ref[key]

            elif token_type == QueryStringToken.KEY:
                try:
                    ref = ref[key]
                    next(tokens)
                # TypeError is for pet[]=lucy&pet[]=ollie
                # if the array key is empty a type error will be raised
                except (IndexError, KeyError, TypeError):
                    # the index didn't exist
                    # so we look ahead to see what we are setting
                    # there is not a next token
                    # set the value
                    try:

                        next_token = next(tokens)

                        if next_token[0] == QueryStringToken.ARRAY:
                            ref.append([])
                            ref = ref[key]
                        elif next_token[0] == QueryStringToken.OBJECT:

                            try:
                                ref[key] = {}
                            except IndexError:
                                ref.append({})

                            ref = ref[key]
                    except StopIteration:
                        try:
                            ref.append(value)
                        except AttributeError:
                            ref[key] = value
                        return

    def tokens(self, key):
        buf = ""
        for char in key:
            if char == "[":
                yield QueryStringToken.ARRAY, buf
                buf = ""

            elif char == ".":
                yield QueryStringToken.OBJECT, buf
                buf = ""

            elif char == "]":
                try:
                    yield QueryStringToken.KEY, int(buf)
                    buf = ""
                except ValueError:
                    yield QueryStringToken.KEY, None
            else:
                buf = buf + char

        if len(buf) > 0:
            yield QueryStringToken.KEY, buf
        else:
            raise StopIteration()
