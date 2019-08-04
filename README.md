[![Build Status](https://travis-ci.org/brandonwillard/python-cons.svg?branch=master)](https://travis-ci.org/brandonwillard/python-cons) [![Coverage Status](https://coveralls.io/repos/github/brandonwillard/python-cons/badge.svg?branch=master)](https://coveralls.io/github/brandonwillard/python-cons?branch=master) [![PyPI](https://img.shields.io/pypi/v/cons)](https://pypi.org/project/cons/)

Python `cons`
==================

An implementation of [`cons`][cons] in Python.

Usage and Design
======================

The `cons` package attempts to emulate the semantics of Lisp/Scheme's `cons` as closely as possible while incorporating all the built-in Python sequence types:
```python
>>> from cons import cons, car, cdr
>>> cons(1, [])
[1]

>>> cons(1, ())
(1,)

>>> cons(1, [2, 3])
[1, 2, 3]

>>> cons(1, "a string")
ConsPair(1 'a string')
```

According to `cons`, `None` corresponds to the empty built-in `list`:
```python
>>> cons(1, None)
[1]
```

The `cons` package follows Scheme-like semantics for empty sequences:
```python
>>> car([])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Not a cons pair

>>> cdr([])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Not a cons pair

```

Features
===========

* Support for the standard Python ordered collection types: i.e. `list`, `tuple`, `Iterator`, `OrderedDict`.
```python
>>> from collections import OrderedDict
>>> cons(('a', 1), OrderedDict())
OrderedDict([('a', 1)])

```
* Existing `cons` behavior is easy to change and new collections are straightforward to add through [`multipledispatch`][md].
* Built-in support for [`unification`][un].
```python
>>> from unification import unify, reify, var
>>> unify([1, 2], cons(var('car'), var('cdr')), {})
{~car: 1, ~cdr: [2]}

>>> reify(cons(1, var('cdr')), {var('cdr'): [2, 3]})
[1, 2, 3]

>>> reify(cons(1, var('cdr')), {var('cdr'): None})
[1]

```

Installation
================

```python
pip install cons
```


[cons]: https://en.wikipedia.org/wiki/Cons
[md]: https://github.com/mrocklin/multipledispatch
[un]: https://github.com/mrocklin/unification
