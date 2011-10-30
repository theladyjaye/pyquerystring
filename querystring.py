# Fancy query string parsing
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

from urlparse import parse_qsl
class QueryStringToken(object):

    ARRAY    = "ARRAY"
    OBJECT   = "OBJECT"
    KEY      = "KEY"
    BEGIN    = "BEGIN"
    

    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.next = None

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
            self.parse(self.tokenize(key), value)
            return
        except ValueError:
            pass
        
        try:
            key.index(".")
            self.parse(self.tokenize(key), value)
            return
        except ValueError:
            pass
        
        self.result[key] = value
    
    def tokenize(self, value):
        # need to be able to look ahead when a KEY is discovered, linked list
        # makes that a possibility. list() or collections.deque() not so much
        first_token = QueryStringToken(QueryStringToken.BEGIN)
        tokens = first_token
        buf = ""
        
        for char in value:
            if char == "[":
                tokens.next = QueryStringToken(QueryStringToken.ARRAY, buf)
                tokens = tokens.next
                buf = ""
            elif char == "]":
                try:
                    tokens.next = QueryStringToken(QueryStringToken.KEY, int(buf))
                except ValueError:
                    tokens.next = QueryStringToken(QueryStringToken.KEY)
                
                tokens = tokens.next
                buf = ""

            elif char == ".":
                tokens.next = QueryStringToken(QueryStringToken.OBJECT, buf)
                tokens = tokens.next
                buf = ""
            else:
                buf = buf + char
        
        if len(buf) > 0:
            tokens.next = QueryStringToken(QueryStringToken.KEY, buf)
            tokens = tokens.next
        
        return first_token.next
    
    def parse(self, token, value):
        origin = self.result 
        ref    = origin

        while token:
            token_type = token.key
            key        = token.value
            
            #print(token.key, token.value)
            #token = token.next
            #continue
            
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
                    token = token.next
                # TypeError is for pet[]=lucy&pet[]=ollie
                # if the array key is empty a type error will be raised
                except (IndexError, KeyError, TypeError) as e:
                    # the index didn't exist
                    # so we look ahead to see what we are setting
                    # there is not a next token
                    # set the value
                    if token.next is None:
                        try:
                            ref.append(value)
                        except AttributeError:
                            ref[key] = value
                        return
                    else:
                        if token.next.key == QueryStringToken.ARRAY:
                            ref.append([])
                            ref = ref[key]
                        elif token.next.key == QueryStringToken.OBJECT:
                            try:
                                ref[key] = {}
                            except IndexError:
                                ref.append({})

                            ref = ref[key]
                        
                        token = token.next.next
                        continue
            token = token.next