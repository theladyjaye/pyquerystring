import unittest
from querystring import QueryStringParser

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
    
    def test_simple_object(self):
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
    
    def test_multidimensional_array(self):
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
    
    def test_multidimensional_array_with_object(self):
        qs = "&id=foo&dog[0][0].name=lucy&dog[0][1].name=radar&bar=baz"
        parser = QueryStringParser(qs)
        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(parser.result["bar"], "baz")
        self.assertEqual(len(parser.result["dog"]), 1)
        self.assertEqual(parser.result["dog"][0][0]["name"], "lucy")
        self.assertEqual(parser.result["dog"][0][1]["name"], "radar")
    
    def test_array_with_object_with_array(self):
        qs = "&id=foo&dog[0].name=lucy&dog[0].attributes[0]=tail&dog[0].attributes[1]=paws&dog[0].attributes[2]=ears&dog[1].name=radar"
        parser = QueryStringParser(qs)
        self.assertEqual(parser.result["id"], "foo")
        self.assertEqual(len(parser.result["dog"]), 2)
        self.assertEqual(parser.result["dog"][0]["name"], "lucy")
        self.assertEqual(len(parser.result["dog"][0]["attributes"]), 3)
        self.assertEqual(len(parser.result["dog"][0]["attributes"]), 3)
        #self.assertEqual(parser.result["dog"][0][1]["name"], "radar")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(QueryStringSuite))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())



    #querystring = "&pets[0].name=lucy&pets[0].type=dog&pets[1].name=ollie&pets[1].type=cat"
    #querystring = "&pets[0][0].name=lucy&pets[0][1].name=ollie"
    #querystring = "&id=foo&dog[2]=dexter&dog[1]=tucker&dog[0]=lucy&cat=ollie&pets[1].name=pogo&pets[1].type=cat&pets[0].name=kiki&pets[0].type=cat&fish.name=robofish&fish.type=fish&person.name[0]=adam&person.name[1]=danica&family.name[0][1]=adam&family.name[0][0]=danica&family.name[1][0]=lucy&family.name[1][1]=ollie"
    #querystring = "&pets[0].name=pogo&pets[0].type=cat"
    #querystring = "&family.name[0][1]=adam&family.name[0][0]=danica&family.name[1][0]=lucy&family.name[1][1]=ollie"
    #querystring = "&family.name[0]=adam&family.name[1]=danica"
    