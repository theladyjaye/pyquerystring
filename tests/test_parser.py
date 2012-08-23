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

import unittest
import context
from pyquerystring import QueryStringParser


class QueryStringSuite(unittest.TestCase):

    def test_simple(self):
        qs = "&id=foo&dog=lucy&cat=ollie"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(parser.result["dog"], "lucy")
        self.assertEqual(parser.result["cat"], "ollie")

    def test_simple_array(self):
        qs = "&id=foo&dog[1]=lucy&dog[0]=tucker"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 2)
        self.assertEqual(parser.result["dog"][0], "tucker")
        self.assertEqual(parser.result["dog"][1], "lucy")

    def test_simple_object_1(self):
        qs = "&id=foo&dog.name=lucy"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(parser.result["dog"]["name"], "lucy")

    def test_simple_object_2(self):
        qs = "&id=foo&dog.name=lucy&dog.color=brown"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(parser.result["dog"]["name"], "lucy")
        self.assertEqual(parser.result["dog"]["color"], "brown")

    def test_object_with_array(self):
        qs = "&id=foo&dog[0].name=lucy&dog[1].name=radar"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 2)
        self.assertEqual(parser.result["dog"][0]["name"], "lucy")
        self.assertEqual(parser.result["dog"][1]["name"], "radar")

    def test_push_array(self):
        qs = "&id=foo&dog[]=z-lucy&dog[]=radar"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 2)
        self.assertEqual(parser.result["dog"][0], "z-lucy")
        self.assertEqual(parser.result["dog"][1], "radar")

    def test_push_array_object(self):
        qs = "&id=foo&dog.name[]=radar&dog.name[]=tucker&dog.name[]=lucy"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]["name"]), 3)
        self.assertEqual(parser.result["dog"]["name"][0], "radar")
        self.assertEqual(parser.result["dog"]["name"][1], "tucker")
        self.assertEqual(parser.result["dog"]["name"][2], "lucy")

    def test_multidimensional_array2x(self):
        qs = "&id=foo&dog[0][0]=lucy&dog[0][1]=radar&dog[1][0]=tucker&dog[1][1]=dexter"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 2)
        self.assertEqual(len(parser.result["dog"][0]), 2)
        self.assertEqual(len(parser.result["dog"][1]), 2)
        self.assertEqual(parser.result["dog"][0][0], "lucy")
        self.assertEqual(parser.result["dog"][0][1], "radar")
        self.assertEqual(parser.result["dog"][1][0], "tucker")
        self.assertEqual(parser.result["dog"][1][1], "dexter")

    def test_multidimensional_array2x_object(self):
        qs = "&id=foo&dog[0][0].name=lucy&dog[0][1].name=ollie&dog[1][0].name=radar"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 2)
        self.assertEqual(parser.result["dog"][0][0]["name"], "lucy")
        self.assertEqual(parser.result["dog"][0][1]["name"], "ollie")
        self.assertEqual(parser.result["dog"][1][0]["name"], "radar")

    def test_multidimensional_array3x(self):
        qs = "&id=foo&dog[0][0][0]=lucy&dog[0][0][1]=radar&dog[0][0][2]=tucker"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"][0][0]), 3)
        self.assertEqual(parser.result["dog"][0][0][0], "lucy")
        self.assertEqual(parser.result["dog"][0][0][1], "radar")
        self.assertEqual(parser.result["dog"][0][0][2], "tucker")

    def test_multidimensional_array_with_object(self):
        qs = "&id=foo&dog[0][0].name=lucy&dog[0][1].name=radar&bar=baz"
        parser = QueryStringParser(qs)
        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(parser.result["bar"], "baz")
        self.assertEqual(len(parser.result["dog"]), 1)
        self.assertEqual(parser.result["dog"][0][0]["name"], "lucy")
        self.assertEqual(parser.result["dog"][0][1]["name"], "radar")

    def test_array_with_object_with_array(self):
        qs = "&id=foo&dog[0].name=lucy&dog[0].attributes[0]=tail&dog[0].attributes[1]=paws&dog[0].attributes[2]=ears&dog[0].attributes[3].type=dog&dog[1].name=radar"
        parser = QueryStringParser(qs)
        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 2)
        self.assertEqual(parser.result["dog"][0]["name"], "lucy")
        self.assertEqual(len(parser.result["dog"][0]["attributes"]), 4)
        self.assertEqual(parser.result["dog"][0]["attributes"][0], "tail")
        self.assertEqual(parser.result["dog"][0]["attributes"][1], "paws")
        self.assertEqual(parser.result["dog"][0]["attributes"][2], "ears")
        self.assertEqual(parser.result["dog"][0]["attributes"][3]["type"], "dog")
        self.assertEqual(parser.result["dog"][1]["name"], "radar")

    def test_mixed1(self):
        qs = "&id=foo&dog[2]=dexter&dog[1]=tucker&dog[0]=lucy&cat=ollie\
&pets[1].name=pogo&pets[1].type=catz&pets[0].name=kiki\
&pets[0].type=cat&fish.name=robofish&fish.type=fishz\
&person.name[0]=adam&person.name[1]=adamz\
&plants.name[0][1]=flower&plants.name[0][0]=tree\
&plants.name[1][0]=willow&plants.name[1][1]=fern\
&end[0][0][0]=lucy&end[0][0][1]=radar&end[0][0][2]=tucker"
        parser = QueryStringParser(qs)

        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 3)
        self.assertEqual(parser.result["dog"][0], "lucy")
        self.assertEqual(parser.result["dog"][1], "tucker")
        self.assertEqual(parser.result["dog"][2], "dexter")
        self.assertEqual(parser.result["cat"], "ollie")
        self.assertEqual(len(parser.result["pets"]), 2)
        self.assertEqual(parser.result["pets"][0]["name"], "kiki")
        self.assertEqual(parser.result["pets"][0]["type"], "cat")
        self.assertEqual(parser.result["pets"][1]["name"], "pogo")
        self.assertEqual(parser.result["pets"][1]["type"], "catz")
        self.assertEqual(parser.result["fish"]["name"], "robofish")
        self.assertEqual(parser.result["fish"]["type"], "fishz")
        self.assertEqual(len(parser.result["person"]["name"]), 2)
        self.assertEqual(parser.result["person"]["name"][0], "adam")
        self.assertEqual(parser.result["person"]["name"][1], "adamz")
        self.assertEqual(len(parser.result["plants"]["name"]), 2)
        self.assertEqual(len(parser.result["plants"]["name"][0]), 2)
        self.assertEqual(len(parser.result["plants"]["name"][1]), 2)
        self.assertEqual(parser.result["plants"]["name"][0][0], "tree")
        self.assertEqual(parser.result["plants"]["name"][0][1], "flower")
        self.assertEqual(parser.result["plants"]["name"][1][0], "willow")
        self.assertEqual(parser.result["plants"]["name"][1][1], "fern")
        self.assertEqual(parser.result["end"][0][0][0], "lucy")
        self.assertEqual(parser.result["end"][0][0][1], "radar")
        self.assertEqual(parser.result["end"][0][0][2], "tucker")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(QueryStringSuite))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
