# pyprotoparser

A Pure Python Protobuf 3 .proto Parser

## Install

```bash
pip install pyprotoparser
```

## Usage

```python
from pprint import pprint
from pyprotoparser import Parser

messages = Parser().parse("""
    syntax = "proto3";

    message SearchRequest {
        string query = 1 [(validate.rules).double = {gte: -90,  lte: 90}];
        optional int32 page_number = 2;
        option foo = "bar";
        int32 results_per_page = 3;
    }
""")

pprint(messages)

"""
{'SearchRequest': Message(name='SearchRequest',
                          fields=[Field(name='query',
                                        type='string',
                                        cardinality=<FieldCardinality.REQUIRED: 'REQUIRED'>,
                                        options=[Option(name='(validate.rules).double',
                                                        value='{gte:-90,lte:90}')]),
                                  Field(name='page_number',
                                        type='int32',
                                        cardinality=<FieldCardinality.OPTIONAL: 'OPTIONAL'>,
                                        options=[]),
                                  Field(name='results_per_page',
                                        type='int32',
                                        cardinality=<FieldCardinality.REQUIRED: 'REQUIRED'>,
                                        options=[])])}
"""
```

## About

`pyprotoparser` is a pure Python implementation of a `.proto` parser. It uses [Buf.build](https://buf.build)'s ANTLR [Proto .g4 files](https://github.com/bufbuild/protobuf.com/tree/main/examples) to generate a Python lexer and parser. The lexer and parser are complete implementations of Proto 2 and 3.

The project also includes a very simple Parser class and data model to make parsing .proto text easier.