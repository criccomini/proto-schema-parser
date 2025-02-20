# Documentation

## Table of Contents

- [`proto_schema_parser`](#proto-schema-parser)
  - [`ast`](#proto-schema-parser-ast)
    - [`FieldCardinality`](#proto-schema-parser-ast-fieldcardinality)
    - [`File`](#proto-schema-parser-ast-file)
    - [`Comment`](#proto-schema-parser-ast-comment)
    - [`Package`](#proto-schema-parser-ast-package)
    - [`Import`](#proto-schema-parser-ast-import)
    - [`MessageLiteralField`](#proto-schema-parser-ast-messageliteralfield)
    - [`MessageLiteral`](#proto-schema-parser-ast-messageliteral)
    - [`Option`](#proto-schema-parser-ast-option)
    - [`Message`](#proto-schema-parser-ast-message)
    - [`Field`](#proto-schema-parser-ast-field)
    - [`MapField`](#proto-schema-parser-ast-mapfield)
    - [`Group`](#proto-schema-parser-ast-group)
    - [`OneOf`](#proto-schema-parser-ast-oneof)
    - [`ExtensionRange`](#proto-schema-parser-ast-extensionrange)
    - [`Reserved`](#proto-schema-parser-ast-reserved)
    - [`Enum`](#proto-schema-parser-ast-enum)
    - [`EnumValue`](#proto-schema-parser-ast-enumvalue)
    - [`EnumReserved`](#proto-schema-parser-ast-enumreserved)
    - [`Extension`](#proto-schema-parser-ast-extension)
    - [`Service`](#proto-schema-parser-ast-service)
    - [`Method`](#proto-schema-parser-ast-method)
    - [`MessageType`](#proto-schema-parser-ast-messagetype)
    - [`Identifier`](#proto-schema-parser-ast-identifier)
  - [`generator`](#proto-schema-parser-generator)
    - [`Generator`](#proto-schema-parser-generator-generator)
      - [`generate`](#proto-schema-parser-generator-generator-generate)
  - [`parser`](#proto-schema-parser-parser)
    - [`Parser`](#proto-schema-parser-parser-parser)
      - [`__init__`](#proto-schema-parser-parser-parser-init)
      - [`parse`](#proto-schema-parser-parser-parser-parse)

<a id="proto-schema-parser"></a>
# `proto_schema_parser`


**Exports:**

- `Parser`
- `Message`
- `Field`
- `Option`
- `FieldCardinality`

<a id="proto-schema-parser-ast"></a>
## `ast`

<a id="proto-schema-parser-ast-fieldcardinality"></a>
### `FieldCardinality`

<a id="proto-schema-parser-ast-file"></a>
### `File`

Represents a .proto file.

<a id="proto-schema-parser-ast-comment"></a>
### `Comment`

Represents a comment in a .proto file.

<a id="proto-schema-parser-ast-package"></a>
### `Package`

Represents a package declaration in a .proto file.

<a id="proto-schema-parser-ast-import"></a>
### `Import`

Represents an import declaration in a .proto file.

<a id="proto-schema-parser-ast-messageliteralfield"></a>
### `MessageLiteralField`

Represents a field in a message literal.

<a id="proto-schema-parser-ast-messageliteral"></a>
### `MessageLiteral`

Represents a message literal.

<a id="proto-schema-parser-ast-option"></a>
### `Option`

Represents an option in a .proto file.

<a id="proto-schema-parser-ast-message"></a>
### `Message`

Represents a message in a .proto file.

<a id="proto-schema-parser-ast-field"></a>
### `Field`

Represents a field in a message.

<a id="proto-schema-parser-ast-mapfield"></a>
### `MapField`

Represents a map field in a message.

<a id="proto-schema-parser-ast-group"></a>
### `Group`

Represents a group in a message.

<a id="proto-schema-parser-ast-oneof"></a>
### `OneOf`

Represents an oneof in a message.

<a id="proto-schema-parser-ast-extensionrange"></a>
### `ExtensionRange`

Represents an extension range in a message.

<a id="proto-schema-parser-ast-reserved"></a>
### `Reserved`

Represents a reserved range or name in a message.

<a id="proto-schema-parser-ast-enum"></a>
### `Enum`

Represents an enum in a message.

<a id="proto-schema-parser-ast-enumvalue"></a>
### `EnumValue`

Represents an enum value in an enum.

<a id="proto-schema-parser-ast-enumreserved"></a>
### `EnumReserved`

Represents a reserved range or name in an enum.

<a id="proto-schema-parser-ast-extension"></a>
### `Extension`

Represents an extension in a message.

<a id="proto-schema-parser-ast-service"></a>
### `Service`

Represents a service in a message.

<a id="proto-schema-parser-ast-method"></a>
### `Method`

Represents a method in a service.

<a id="proto-schema-parser-ast-messagetype"></a>
### `MessageType`

Represents a message type in a message.

<a id="proto-schema-parser-ast-identifier"></a>
### `Identifier`

Identifier is a simple dataclass to represent an unquoted identifier (such

as an enumerator name). It's used as a value for scalar types that can't be
parsed into a string, int, float, or bool.

<a id="proto-schema-parser-generator"></a>
## `generator`

<a id="proto-schema-parser-generator-generator"></a>
### `Generator`

Generator class that takes an abstract syntax tree (AST) and

generates a protobuf schema string.

<a id="proto-schema-parser-generator-generator-generate"></a>
#### `generate`

```python
def generate(self, file: ast.File) -> str:
```

Generates a protobuf schema string from an abstract syntax tree (AST).

**Args:**

- `file` (*ast.File*): The abstract syntax tree of the .proto file.

**Returns:** (*str*) The generated protobuf schema string.

<a id="proto-schema-parser-parser"></a>
## `parser`

<a id="proto-schema-parser-parser-parser"></a>
### `Parser`

Parser class that takes a string representing a protobuf schema and returns an

abstract syntax tree (AST).

<a id="proto-schema-parser-parser-parser-init"></a>
#### `__init__`

```python
def __init__(self, *, setup_lexer: Optional[SetupLexerCb], setup_parser: Optional[SetupParserCb]) -> None:
```

Initializes a new instance of the Parser class.

**Args:**

- `setup_lexer` (*Optional[SetupLexerCb]*): A callback function to
modify the lexer during parsing. Defaults to None.
- `setup_parser` (*Optional[SetupParserCb]*): A callback function
to modify the parser during parsing. Defaults to None.

<a id="proto-schema-parser-parser-parser-parse"></a>
#### `parse`

```python
def parse(self, text: str) -> ast.File:
```

Parses a string representing a protobuf schema and returns an abstract syntax tree (AST).

**Args:**

- `text` (*str*): The string representing the protobuf schema.

**Returns:** (*ast.File*) The abstract syntax tree representation of the protobuf schema.
