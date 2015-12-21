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

# Path hack.

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from pyquerystring import parse


class QueryStringSuite(unittest.TestCase):

    def test_simple(self):
        qs = "&id=foo&dog=lucy&cat=ollie"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(result["dog"], "lucy")
        self.assertEqual(result["cat"], "ollie")

    def test_simple_array_with_spaces(self):
        qs = "&id=foo& dog[1] = lucy& dog[0] = tucker"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 2)
        self.assertEqual(result["dog"][0], "tucker")
        self.assertEqual(result["dog"][1], "lucy")

    def test_bad_format(self):
        qs = "&id=foo&dog[1]]=lucy"
        with self.assertRaises(IOError):
            parse(qs)

    def test_overlaping_keys(self):
        qs = "&id=foo&id=foo2"
        result = parse(qs)
        self.assertEqual(result["id"], "foo2")

    def test_overlaping_array_keys(self):
        qs = "&id[1]=foo&id[1]=foo2"
        result = parse(qs)
        self.assertEqual(result["id"][1], "foo2")

    def test_overlaping_array_objects(self):
        qs = "&id[1].name=foo&id[1].name=foo2"
        result = parse(qs)
        self.assertEqual(result["id"][1]['name'], "foo2")

    def test_simple_array(self):
        qs = "&id=foo&dog[1]=lucy&dog[0]=tucker"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 2)
        self.assertEqual(result["dog"][0], "tucker")
        self.assertEqual(result["dog"][1], "lucy")

    def test_simple_object_1(self):
        qs = "&id=foo&dog.name=lucy"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(result["dog"]["name"], "lucy")

    def test_simple_object_2(self):
        qs = "&id=foo&dog.name=lucy&dog.color=brown"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(result["dog"]["name"], "lucy")
        self.assertEqual(result["dog"]["color"], "brown")

    def test_simple_object_3(self):
        qs = "&id=foo&dog.name=lucy&dog[color]=brown"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(result["dog"]["name"], "lucy")
        self.assertEqual(result["dog"]["color"], "brown")

    def test_simple_object_4(self):
        qs = "&id=foo&dog2[name]=lucy&dog2[name2]=lucy&dog[ color ]=brown"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(result["dog2"]["name2"], "lucy")
        self.assertEqual(result["dog"]["color"], "brown")

    def test_odd_names(self):
        qs = "&id=foo&dog[name.1]=lucy&dog[name[2]]=radar"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(result["dog"]["name.1"], "lucy")
        self.assertEqual(result["dog"]["name[2]"], "radar")

    def test_object_with_array(self):
        qs = "&id=foo&dog[0].name=lucy&dog[1].name=radar"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 2)
        self.assertEqual(result["dog"][0]["name"], "lucy")
        self.assertEqual(result["dog"][1]["name"], "radar")

    def test_push_array(self):
        qs = "&id=foo&dog[]=z-lucy&dog[]=radar"
        result = parse(qs)
        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 2)
        self.assertEqual(result["dog"][0], "z-lucy")
        self.assertEqual(result["dog"][1], "radar")

    def test_push_array_object(self):
        qs = "&id=foo&dog.name[]=radar&dog.name[]=tucker&dog.name[]=lucy"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]["name"]), 3)
        self.assertEqual(result["dog"]["name"][0], "radar")
        self.assertEqual(result["dog"]["name"][1], "tucker")
        self.assertEqual(result["dog"]["name"][2], "lucy")

    def test_multidimensional_array2x(self):
        qs = "&id=foo&dog[0][0]=lucy&dog[0][1]=radar&dog[1][0]=tucker&dog[1][1]=dexter"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 2)
        self.assertEqual(len(result["dog"][0]), 2)
        self.assertEqual(len(result["dog"][1]), 2)
        self.assertEqual(result["dog"][0][0], "lucy")
        self.assertEqual(result["dog"][0][1], "radar")
        self.assertEqual(result["dog"][1][0], "tucker")
        self.assertEqual(result["dog"][1][1], "dexter")

    def test_multidimensional_array2x_object(self):
        qs = "&id=foo&dog[0][0].name=lucy&dog[0][1].name=ollie&dog[1][0].name=radar"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 2)
        self.assertEqual(result["dog"][0][0]["name"], "lucy")
        self.assertEqual(result["dog"][0][1]["name"], "ollie")
        self.assertEqual(result["dog"][1][0]["name"], "radar")

    def test_multidimensional_array3x(self):
        qs = "&id=foo&dog[0][0][0]=lucy&dog[0][0][1]=radar&dog[0][0][2]=tucker"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"][0][0]), 3)
        self.assertEqual(result["dog"][0][0][0], "lucy")
        self.assertEqual(result["dog"][0][0][1], "radar")
        self.assertEqual(result["dog"][0][0][2], "tucker")

    def test_multidimensional_array_with_object(self):
        qs = "&id=foo&dog[0][0].name=lucy&dog[0][1].name=radar&bar=baz"
        result = parse(qs)
        self.assertEqual(result["id"], "foo")
        self.assertEqual(result["bar"], "baz")
        self.assertEqual(len(result["dog"]), 1)
        self.assertEqual(result["dog"][0][0]["name"], "lucy")
        self.assertEqual(result["dog"][0][1]["name"], "radar")

    def test_array_with_object_with_array(self):
        qs = "&id=foo&dog[0].name=lucy&dog[0].attributes[0]=tail&dog[0].attributes[1]=paws&dog[0].attributes[2]=ears&dog[0].attributes[3].type=dog&dog[1].name=radar"
        result = parse(qs)
        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 2)
        self.assertEqual(result["dog"][0]["name"], "lucy")
        self.assertEqual(len(result["dog"][0]["attributes"]), 4)
        self.assertEqual(result["dog"][0]["attributes"][0], "tail")
        self.assertEqual(result["dog"][0]["attributes"][1], "paws")
        self.assertEqual(result["dog"][0]["attributes"][2], "ears")
        self.assertEqual(result["dog"][0]["attributes"][3]["type"], "dog")
        self.assertEqual(result["dog"][1]["name"], "radar")

    def test_mixed1(self):
        qs = "&id=foo&dog[2]=dexter&dog[1]=tucker&dog[0]=lucy&cat=ollie\
&pets[1].name=pogo&pets[1].type=catz&pets[0].name=kiki\
&pets[0].type=cat&fish.name=robofish&fish.type=fishz\
&person.name[0]=adam&person.name[1]=adamz\
&plants.name[0][1]=flower&plants.name[0][0]=tree\
&plants.name[1][0]=willow&plants.name[1][1]=fern\
&end[0][0][0]=lucy&end[0][0][1]=radar&end[0][0][2]=tucker"
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 3)
        self.assertEqual(result["dog"][0], "lucy")
        self.assertEqual(result["dog"][1], "tucker")
        self.assertEqual(result["dog"][2], "dexter")
        self.assertEqual(result["cat"], "ollie")
        self.assertEqual(len(result["pets"]), 2)
        self.assertEqual(result["pets"][0]["name"], "kiki")
        self.assertEqual(result["pets"][0]["type"], "cat")
        self.assertEqual(result["pets"][1]["name"], "pogo")
        self.assertEqual(result["pets"][1]["type"], "catz")
        self.assertEqual(result["fish"]["name"], "robofish")
        self.assertEqual(result["fish"]["type"], "fishz")
        self.assertEqual(len(result["person"]["name"]), 2)
        self.assertEqual(result["person"]["name"][0], "adam")
        self.assertEqual(result["person"]["name"][1], "adamz")
        self.assertEqual(len(result["plants"]["name"]), 2)
        self.assertEqual(len(result["plants"]["name"][0]), 2)
        self.assertEqual(len(result["plants"]["name"][1]), 2)
        self.assertEqual(result["plants"]["name"][0][0], "tree")
        self.assertEqual(result["plants"]["name"][0][1], "flower")
        self.assertEqual(result["plants"]["name"][1][0], "willow")
        self.assertEqual(result["plants"]["name"][1][1], "fern")
        self.assertEqual(result["end"][0][0][0], "lucy")
        self.assertEqual(result["end"][0][0][1], "radar")
        self.assertEqual(result["end"][0][0][2], "tucker")


    def test_list_gap(self):
        qs = "&id=foo&dog[2]=dexter&cat=ollie"
        result = parse(qs)
        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 3)
        self.assertEqual(result["dog"][0], None)
        self.assertEqual(result["dog"][1], None)
        self.assertEqual(result["dog"][2], "dexter")
        self.assertEqual(result["cat"], "ollie")


    def test_lotsa_items(self):
        qs = (
            "&id=foo&dog[2]=dexter&dog[1]=tucker&dog[0]=lucy&dog[3]=lucy"
            "&dog[4]=lucy&dog[5]=lucy&dog[6]=lucy&dog[7]=lucy&dog[8]=lucy"
            "&dog[9]=lucy&dog[10]=fido&dog[11]=lucyagain"
        )
        result = parse(qs)

        self.assertEqual(result["id"], "foo")
        self.assertEqual(len(result["dog"]), 12)
        self.assertEqual(result["dog"][0], "lucy")
        self.assertEqual(result["dog"][1], "tucker")
        self.assertEqual(result["dog"][2], "dexter")
        self.assertEqual(result["dog"][3], "lucy")
        self.assertEqual(result["dog"][4], "lucy")
        self.assertEqual(result["dog"][5], "lucy")
        self.assertEqual(result["dog"][10], "fido")
        self.assertEqual(result["dog"][11], "lucyagain")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(QueryStringSuite))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
