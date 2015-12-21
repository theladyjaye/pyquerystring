# Query String Parsing The Way It Should Be

[![Build Status](https://secure.travis-ci.org/aventurella/pyquerystring.png?branch=master)](http://travis-ci.org/aventurella/pyquerystring)

## The Problem

Python's default `urlparse.parse_qs()` does not understand the concept of data structures.  The standard behavior of parse_qs is as follows:

```js
    // parse_qs("dog=lucy&dog=tucker&dog=radar&id=11")
	{"dog": ["lucy", "tucer", "radar"], "id":[11]}
```

While this works for simple querystrings, anything more complex returns a less than desirable result.

```js
	// parse_qs("dog[0]=lucy&dog[1]=tucker&dog[2]=radar&id=11")
	{"dog[0]":["lucy"], "dog[1]":["tucker"], "dog[2]":["radar"], "id":[11]}
```

This library is intended to intelligently parse complex querystrings that python's library is unable to handle such as the following:

```
mylist[]=item0&mylist[]=item1
mylist[0]=item0&mylist[1]=item1
mylist[0][0]=subitem0&mylist[0][1]=subitem1
mylist.element=item0
mylist.element[0]=item0&mylist.element[1]=item0
```

## How it works

Lets try some code:

```python
	>>> from pyquerystring import parse
	>>> qs = "id=foo&dog[0].name=lucy&dog[1].name=radar"
	>>> result = parse(qs)
	>>> print(result["dog"][0]["name"])
	lucy
	>>> print(result)
	{'id': 'foo', 'dog': [{'name': 'lucy'}, {'name': 'radar'}]}
```

You can also do some primitive array pushing:

```python
	>>> parse("dog[]=radar&dog[]=lucy&dog[]=tucker")
	{'dog': ['radar', 'lucy', 'tucker']}
	>>> parse("dog.name[]=radar&dog.name[]=tucker&dog.name[]=lucy")
	{'dog': {'name': ['radar', 'tucker', 'lucy']}}
```

You can pass objects by associative array or dot notation:

```python
	>>> parse("dog[name]=radar")
	{'dog': {'name': 'radar'}}
	>>> parse("dog.name=radar")
	{'dog': {'name': 'radar'}}
```

You can get pretty crazy with it as well.  It will handle multidimensional arrays:

```python
	>>> parse("dog[0][0]=lucy&dog[0][1]=radar&dog[1][0]=tucker&dog[1][1]=dexter")
	{'dog': [['lucy', 'radar'], ['tucker', 'dexter']]}
```

Or you can go totally nuts and just throw some mixed madness at it:

```python
	>>> parse("dog[1]=tucker&dog[0]=lucy&pets[1].name=pogo&pets[1].type=catz&pets[0].name=kiki&pets[0].type=cat&fish.name=robofish&fish.type=fishz&person.name[0]=adam&person.name[1]=adamz&plants.name[0][1]=flower&plants.name[0][0]=tree&plants.name[1][0]=willow&plants.name[1][1]=fern")
	{'plants': {'name': [['tree', 'flower'], ['willow', 'fern']]}, 'fish': {'type': 'fishz', 'name': 'robofish'}, 'dog': ['lucy', 'tucker'], 'person': {'name': ['adam', 'adamz']}, 'pets': [{'type': 'cat', 'name': 'kiki'}, {'type': 'catz', 'name': 'pogo'}]}
```




For more examples, crack open tests/test_parser.py to see some additional examples.
