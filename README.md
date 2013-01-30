# Fancy Query String or application/x-www-form-urlencoded parsing

[![Build Status](https://secure.travis-ci.org/aventurella/pyquerystring.png?branch=master)](http://travis-ci.org/aventurella/pyquerystring)

## The Problem

Python's default:

```python
	from urlparse import parse_qsl
	from urlparse import parse_qs
```

does not understand the concept of data structures. When given a query string of:

	&dog=lucy&dog=tucker&dog=radar&id=11

*parse_qs* will return something like this:

```json
	{"dog":["lucy", "tucer", "radar"], "id":[11]}
```

This is perfect for simple things. If you wanted to communicate a more complex data structure:

	&dog[0]=lucy&dog[1]=tucker&dog[2]=radar&id=11

*parse_qs* will give you back something like:

```json
	{"dog[0]":["lucy"], "dog[1]":["tucker"], "dog[2]":["radar"], "id":[11]}
```

Not exactly what was described by the query string.  But that's ok, if you need fancier query strings or application/x-www-form-urlencoded parsing this library to the rescue.

## How it works

Lets try some code:

```python
	from querystring import parse

	def __main__():
		qs = "&id=foo&dog[0].name=lucy&dog[1].name=radar"
		result = parse(qs)
		print(result["dog"][0]["name"]) #lucy
		print(result["dog"][1]["name"]) #radar

	if __name__ == "__main__":
		main()
```

In other words, you get this:

```json
	{"id":"foo",
	 "dog":[{"name":"lucy"}, {"name":"radar"}]
	}
```
You can get pretty crazy with it as well.  It will handle multidimensional arrays:

	&id=foo&dog[0][0]=lucy&dog[0][1]=radar&dog[1][0]=tucker&dog[1][1]=dexter

even 3 dimensional arrays:

	&id=foo&dog[0][0][0]=lucy&dog[0][0][1]=radar&dog[0][0][2]=tucker

Or you can go totally nuts and just throw some mixed madness at it:

	&id=foo&dog[2]=dexter&dog[1]=tucker&dog[0]=lucy&cat=ollie&pets[1].name=pogo&pets[1].type=catz&pets[0].name=kiki&pets[0].type=cat&fish.name=robofish&fish.type=fishz&person.name[0]=adam&person.name[1]=adamz&plants.name[0][1]=flower&plants.name[0][0]=tree&plants.name[1][0]=willow&plants.name[1][1]=fern

You can also do some primitive array pushing:

	&id=foo&dog[]=radar&dog[]=lucy&dog[]=tucker

Or push into an object:

	&id=foo&dog.name[]=radar&dog.name[]=tucker&dog.name[]=lucy

And you would get:

```json
	{"id":"foo",
    "dog":{"name":["radar", "tucker", "lucy"]}
   }
```
Anyway, I think you get the idea. Crack open tests/test_parser.py if you would like to see some additional examples.

P.S. You could apply this to multipart parsing as well, you would just need to extract the parts that are not files, and hand them to this query string parser.
