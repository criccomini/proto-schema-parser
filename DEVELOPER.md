# Developer Notes

## Generating Lexer/Parser

The lexer and parser come from  [Buf](https://buf.build/)'s ANTLR [lexer and parser](https://github.com/bufbuild/protobuf.com/tree/main/examples/antlr) grammar files.

_NOTE: I've chosen to check the files into the `antlr` directory rather than use a git submodule because the files are in a subfolder and ANTLR's `org.antlr.v4.Tool` doesn't have a good way to put the generated content into `proto_schema_parser/antlr`. Keeping things flat means that the Python files are placed in proper Python package directory._

To generate the lexer and parser, run the following:

```bash
pdm run antlr
```

## Releasing

Pypi publication can be done with:

```bash
pdm run publish
```

Don't forget to create a Github release and bump the version number after.