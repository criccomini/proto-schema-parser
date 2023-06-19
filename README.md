# Protobuf Schema Parser

A Pure Python Protobuf 3 .proto schema Parser

## Install

```bash
pip install proto-schema-parser
```

## Usage

```python
from pprint import pprint
from proto_schema_parser import Parser

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

`proto-schema-parser` is a pure Python implementation of a `.proto` parser. It uses [Buf.build](https://buf.build)'s ANTLR [Proto .g4 files](https://github.com/bufbuild/protobuf.com/tree/main/examples/antlr) to generate a Python Protocol buffer lexer and parser. The lexer and parser are complete implementations of Proto 2 and 3.

The project also includes a very simple Parser class and data model to make parsing .proto text easier.