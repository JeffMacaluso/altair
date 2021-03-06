# The contents of this file are automatically written by
# tools/generate_schema_wrapper.py. Do not modify directly
# 2018-02-20 10:30:19
import jsonschema
import pytest

from ..schemapi import UndefinedType, SchemaBase, Undefined


class MySchema(SchemaBase):
    _schema = {
        'definitions': {
            'StringMapping': {'type': 'object', 'additionalProperties': {'type': 'string'}},
            'StringArray': {'type': 'array', 'items': {'type': 'string'}}
        },
        'properties': {
            'a': {'$ref': '#/definitions/StringMapping'},
            'a2': {'type': 'object', 'additionalProperties': {'type': 'number'}},
            'b': {'$ref': '#/definitions/StringArray'},
            'b2': {'type': 'array', 'items': {'type': 'number'}},
            'c': {'type': ['string', 'number']},
            'd': {'anyOf': [{'$ref': '#/definitions/StringMapping'},
                            {'$ref': '#/definitions/StringArray'}]}
        }
    }


class StringMapping(SchemaBase):
    _schema = {'$ref': '#/definitions/StringMapping'}
    _rootschema = MySchema._schema


class StringArray(SchemaBase):
    _schema = {'$ref': '#/definitions/StringArray'}
    _rootschema = MySchema._schema


class Derived(SchemaBase):
    _schema = {
        'definitions': {
            'Foo': {
                'type': 'object',
                'properties': {
                    'd': {'type': 'string'}
                }
            },
            'Bar': {'type': 'string', 'enum': ['A', 'B']}
        },
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'a': {'type': 'integer'},
            'b': {'type': 'string'},
            'c': {"$ref": "#/definitions/Foo"}
        }
    }


class Foo(SchemaBase):
    _schema = {"$ref": "#/definitions/Foo"}
    _rootschema = Derived._schema


class Bar(SchemaBase):
    _schema = {"$ref": "#/definitions/Bar"}
    _rootschema = Derived._schema


class SimpleUnion(SchemaBase):
    _schema = {'anyOf' : [{'type': 'integer'}, {'type': 'string'}]}


class DefinitionUnion(SchemaBase):
    _schema = {
        "anyOf": [
            {"$ref": "#/definitions/Foo"},
            {"$ref": "#/definitions/Bar"}
        ]
    }
    _rootschema = Derived._schema


class SimpleArray(SchemaBase):
    _schema = {
        'type': 'array',
        'items': {
            'anyOf' : [{'type': 'integer'}, {'type': 'string'}]
        }
    }


class InvalidProperties(SchemaBase):
    _schema = {
        'type': 'object',
        'properties': {
            'for': {},
            'as': {},
            'vega-lite': {},
            '$schema': {}
        }
    }


def test_construct_multifaceted_schema():
    dct = {'a': {'foo': 'bar'}, 'a2': {'foo': 42},
       'b': ['a', 'b', 'c'], 'b2': [1, 2, 3], 'c': 42,
       'd': ['x', 'y', 'z']}

    myschema = MySchema.from_dict(dct)
    assert myschema.to_dict() == dct

    myschema2 = MySchema(**dct)
    assert myschema2.to_dict() == dct

    assert isinstance(myschema.a, StringMapping)
    assert isinstance(myschema.a2, dict)
    assert isinstance(myschema.b, StringArray)
    assert isinstance(myschema.b2, list)
    assert isinstance(myschema.d, StringArray)


def test_schema_cases():
    assert Derived(a=4, b='yo').to_dict() == {'a': 4, 'b': 'yo'}
    assert Derived(a=4, c={'d': 'hey'}).to_dict() == {'a': 4, 'c': {'d': 'hey'}}
    assert Derived(a=4, b='5', c=Foo(d='val')).to_dict() == {'a': 4, 'b': '5', 'c': {'d': 'val'}}
    assert Foo(d='hello', f=4).to_dict() == {'d': 'hello', 'f': 4}

    assert Derived().to_dict() == {}
    assert Foo().to_dict() == {}

    with pytest.raises(jsonschema.ValidationError):
        # a needs to be an integer
        Derived(a='yo').to_dict()

    with pytest.raises(jsonschema.ValidationError):
        # Foo.d needs to be a string
        Derived(c=Foo(4)).to_dict()

    with pytest.raises(jsonschema.ValidationError):
        # no additional properties allowed
        Derived(foo='bar').to_dict()


def test_round_trip():
    D = {'a': 4, 'b': 'yo'}
    assert Derived.from_dict(D).to_dict() == D

    D = {'a': 4, 'c': {'d': 'hey'}}
    assert Derived.from_dict(D).to_dict() == D

    D = {'a': 4, 'b': '5', 'c': {'d': 'val'}}
    assert Derived.from_dict(D).to_dict() == D

    D = {'d': 'hello', 'f': 4}
    assert Foo.from_dict(D).to_dict() == D


def test_from_dict():
    D = {'a': 4, 'b': '5', 'c': {'d': 'val'}}
    obj = Derived.from_dict(D)
    assert obj.a == 4
    assert obj.b == '5'
    assert isinstance(obj.c, Foo)


def test_simple_type():
    assert SimpleUnion(4).to_dict() == 4


def test_simple_array():
    assert SimpleArray([4, 5, 'six']).to_dict() == [4, 5, 'six']
    assert SimpleArray.from_dict(list('abc')).to_dict() == list('abc')


def test_definition_union():
    obj = DefinitionUnion.from_dict("A")
    assert isinstance(obj, Bar)
    assert obj.to_dict() == "A"

    obj = DefinitionUnion.from_dict("B")
    assert isinstance(obj, Bar)
    assert obj.to_dict() == "B"

    obj = DefinitionUnion.from_dict({'d': 'yo'})
    assert isinstance(obj, Foo)
    assert obj.to_dict() == {'d': 'yo'}


def test_invalid_properties():
    dct = {'for': 2, 'as': 3, 'vega-lite': 4, '$schema': 5}
    invalid = InvalidProperties.from_dict(dct)
    assert invalid['for'] == 2
    assert invalid['as'] == 3
    assert invalid['vega-lite'] == 4
    assert invalid['$schema'] == 5
    assert invalid.to_dict() == dct


def test_undefined_singleton():
    assert Undefined is UndefinedType()


def test_copy():
    dct = {'a': {'foo': 'bar'}, 'a2': {'foo': 42},
       'b': ['a', 'b', 'c'], 'b2': [1, 2, 3], 'c': 42,
       'd': ['x', 'y', 'z']}

    myschema = MySchema.from_dict(dct)

    # Make sure copy is deep
    copy = myschema.copy(deep=True)
    copy['a']['foo'] = 'new value'
    copy['b'] = ['A', 'B', 'C']
    copy['c'] = 164
    assert myschema.to_dict() == dct

    # If we ignore a value, changing the copy changes the original
    copy = myschema.copy(deep=True, ignore=['a'])
    copy['a']['foo'] = 'new value'
    copy['b'] = ['A', 'B', 'C']
    copy['c'] = 164
    mydct = myschema.to_dict()
    assert mydct['a']['foo'] == 'new value'
    assert mydct['b'][0] == dct['b'][0]
    assert mydct['c'] == dct['c']

    # If copy is not deep, then changing copy below top level changes original
    copy = myschema.copy(deep=False)
    copy['a']['foo'] = 'baz'
    copy['b'] = ['A', 'B', 'C']
    copy['c'] = 164
    mydct = myschema.to_dict()
    assert mydct['a']['foo'] == 'baz'
    assert mydct['b'] == dct['b']
    assert mydct['c'] == dct['c']
