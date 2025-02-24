# `proto_schema_parser`

## Table of Contents

- 🅼 [proto\_schema\_parser](#proto_schema_parser)
- 🅼 [proto\_schema\_parser\.ast](#proto_schema_parser-ast)
- 🅼 [proto\_schema\_parser\.generator](#proto_schema_parser-generator)
- 🅼 [proto\_schema\_parser\.parser](#proto_schema_parser-parser)

<a name="proto_schema_parser"></a>
## 🅼 proto\_schema\_parser

- **[Exports](#proto_schema_parser-exports)**

<a name="proto_schema_parser-exports"></a>
### Exports

- 🅼 [`Parser`](#proto_schema_parser-Parser)
- 🅼 [`Message`](#proto_schema_parser-Message)
- 🅼 [`Field`](#proto_schema_parser-Field)
- 🅼 [`Option`](#proto_schema_parser-Option)
- 🅼 [`FieldCardinality`](#proto_schema_parser-FieldCardinality)
<a name="proto_schema_parser-ast"></a>
## 🅼 proto\_schema\_parser\.ast

- **Classes:**
  - 🅲 [FieldCardinality](#proto_schema_parser-ast-FieldCardinality)
  - 🅲 [File](#proto_schema_parser-ast-File)
  - 🅲 [Comment](#proto_schema_parser-ast-Comment)
  - 🅲 [Package](#proto_schema_parser-ast-Package)
  - 🅲 [Import](#proto_schema_parser-ast-Import)
  - 🅲 [MessageLiteralField](#proto_schema_parser-ast-MessageLiteralField)
  - 🅲 [MessageLiteral](#proto_schema_parser-ast-MessageLiteral)
  - 🅲 [Option](#proto_schema_parser-ast-Option)
  - 🅲 [Message](#proto_schema_parser-ast-Message)
  - 🅲 [Field](#proto_schema_parser-ast-Field)
  - 🅲 [MapField](#proto_schema_parser-ast-MapField)
  - 🅲 [Group](#proto_schema_parser-ast-Group)
  - 🅲 [OneOf](#proto_schema_parser-ast-OneOf)
  - 🅲 [ExtensionRange](#proto_schema_parser-ast-ExtensionRange)
  - 🅲 [Reserved](#proto_schema_parser-ast-Reserved)
  - 🅲 [Enum](#proto_schema_parser-ast-Enum)
  - 🅲 [EnumValue](#proto_schema_parser-ast-EnumValue)
  - 🅲 [EnumReserved](#proto_schema_parser-ast-EnumReserved)
  - 🅲 [Extension](#proto_schema_parser-ast-Extension)
  - 🅲 [Service](#proto_schema_parser-ast-Service)
  - 🅲 [Method](#proto_schema_parser-ast-Method)
  - 🅲 [MessageType](#proto_schema_parser-ast-MessageType)
  - 🅲 [Identifier](#proto_schema_parser-ast-Identifier)

### Classes

<a name="proto_schema_parser-ast-FieldCardinality"></a>
### 🅲 proto\_schema\_parser\.ast\.FieldCardinality

```python
class FieldCardinality(str, PyEnum):
```
<a name="proto_schema_parser-ast-File"></a>
### 🅲 proto\_schema\_parser\.ast\.File

```python
class File:
```

Represents a \.proto file\.

**Attributes:**

- **syntax**: Union\[str, None\]
The syntax level of the \.proto file\.
- **file_elements**: List\[FileElement\]
A list of file elements in the \.proto file\.
<a name="proto_schema_parser-ast-Comment"></a>
### 🅲 proto\_schema\_parser\.ast\.Comment

```python
class Comment:
```

Represents a comment in a \.proto file\.

**Attributes:**

- **text**: str
The text of the comment\.
<a name="proto_schema_parser-ast-Package"></a>
### 🅲 proto\_schema\_parser\.ast\.Package

```python
class Package:
```

Represents a package declaration in a \.proto file\.

**Attributes:**

- **name**: str
The name of the package\.
<a name="proto_schema_parser-ast-Import"></a>
### 🅲 proto\_schema\_parser\.ast\.Import

```python
class Import:
```

Represents an import declaration in a \.proto file\.

**Attributes:**

- **name**: str
The name of the imported file\.
- **weak**: bool
True if the import is weak, False otherwise\.
- **public**: bool
True if the import is public, False otherwise\.
<a name="proto_schema_parser-ast-MessageLiteralField"></a>
### 🅲 proto\_schema\_parser\.ast\.MessageLiteralField

```python
class MessageLiteralField:
```

Represents a field in a message literal\.

**Attributes:**

- **name**: str
The name of the field\.
- **value**: MessageValue
The value of the field\.
<a name="proto_schema_parser-ast-MessageLiteral"></a>
### 🅲 proto\_schema\_parser\.ast\.MessageLiteral

```python
class MessageLiteral:
```

Represents a message literal\.

**Attributes:**

- **fields**: List\[MessageLiteralField\]
The fields of the message literal\.
<a name="proto_schema_parser-ast-Option"></a>
### 🅲 proto\_schema\_parser\.ast\.Option

```python
class Option:
```

Represents an option in a \.proto file\.

**Attributes:**

- **name**: str
The name of the option\.
- **value**: Union\[ScalarValue, MessageLiteral\]
The value of the option\.
<a name="proto_schema_parser-ast-Message"></a>
### 🅲 proto\_schema\_parser\.ast\.Message

```python
class Message:
```

Represents a message in a \.proto file\.

**Attributes:**

- **name**: str
The name of the message\.
- **elements**: List\[MessageElement\]
The elements of the message\.
<a name="proto_schema_parser-ast-Field"></a>
### 🅲 proto\_schema\_parser\.ast\.Field

```python
class Field:
```

Represents a field in a message\.

**Attributes:**

- **name**: str
The name of the field\.
- **number**: int
The number of the field\.
- **type**: str
The type of the field\.
- **cardinality**: Union\[FieldCardinality, None\] = None
The cardinality of the field\.
- **options**: List\[Option\] = field\(default\_factory=list\)
The options of the field\.
<a name="proto_schema_parser-ast-MapField"></a>
### 🅲 proto\_schema\_parser\.ast\.MapField

```python
class MapField:
```

Represents a map field in a message\.

**Attributes:**

- **name**: str
The name of the field\.
- **number**: int
The number of the field\.
- **key_type**: str
The type of the key\.
- **value_type**: str
The type of the value\.
- **options**: List\[Option\] = field\(default\_factory=list\)
The options of the field\.
<a name="proto_schema_parser-ast-Group"></a>
### 🅲 proto\_schema\_parser\.ast\.Group

```python
class Group:
```

Represents a group in a message\.

**Attributes:**

- **name**: str
The name of the group\.
- **number**: int
The number of the group\.
- **cardinality**: Union\[FieldCardinality, None\] = None
The cardinality of the group\.
- **elements**: List\[MessageElement\] = field\(default\_factory=list\)
The elements of the group\.
<a name="proto_schema_parser-ast-OneOf"></a>
### 🅲 proto\_schema\_parser\.ast\.OneOf

```python
class OneOf:
```

Represents an oneof in a message\.

**Attributes:**

- **name**: str
The name of the oneof\.
- **elements**: List\[OneOfElement\] = field\(default\_factory=list\)
The elements of the oneof\.
<a name="proto_schema_parser-ast-ExtensionRange"></a>
### 🅲 proto\_schema\_parser\.ast\.ExtensionRange

```python
class ExtensionRange:
```

Represents an extension range in a message\.

**Attributes:**

- **ranges**: List\[str\]
The ranges of the extension\.
- **options**: List\[Option\] = field\(default\_factory=list\)
The options of the extension\.
<a name="proto_schema_parser-ast-Reserved"></a>
### 🅲 proto\_schema\_parser\.ast\.Reserved

```python
class Reserved:
```

Represents a reserved range or name in a message\.

**Attributes:**

- **ranges**: List\[str\]
The ranges of the reserved field\.
- **names**: List\[str\]
The names of the reserved field\.
<a name="proto_schema_parser-ast-Enum"></a>
### 🅲 proto\_schema\_parser\.ast\.Enum

```python
class Enum:
```

Represents an enum in a message\.

**Attributes:**

- **name**: str
The name of the enum\.
- **elements**: List\[EnumElement\] = field\(default\_factory=list\)
The elements of the enum\.
<a name="proto_schema_parser-ast-EnumValue"></a>
### 🅲 proto\_schema\_parser\.ast\.EnumValue

```python
class EnumValue:
```

Represents an enum value in an enum\.

**Attributes:**

- **name**: str
The name of the enum value\.
- **number**: int
The number of the enum value\.
- **options**: List\[Option\] = field\(default\_factory=list\)
The options of the enum value\.
<a name="proto_schema_parser-ast-EnumReserved"></a>
### 🅲 proto\_schema\_parser\.ast\.EnumReserved

```python
class EnumReserved:
```

Represents a reserved range or name in an enum\.

**Attributes:**

- **ranges**: List\[str\]
The ranges of the reserved field\.
- **names**: List\[str\]
The names of the reserved field\.
<a name="proto_schema_parser-ast-Extension"></a>
### 🅲 proto\_schema\_parser\.ast\.Extension

```python
class Extension:
```

Represents an extension in a message\.

**Attributes:**

- **typeName**: str
The type name of the extension\.
- **elements**: List\[ExtensionElement\] = field\(default\_factory=list\)
The elements of the extension\.
<a name="proto_schema_parser-ast-Service"></a>
### 🅲 proto\_schema\_parser\.ast\.Service

```python
class Service:
```

Represents a service in a message\.

**Attributes:**

- **name**: str
The name of the service\.
- **elements**: List\[ServiceElement\] = field\(default\_factory=list\)
The elements of the service\.
<a name="proto_schema_parser-ast-Method"></a>
### 🅲 proto\_schema\_parser\.ast\.Method

```python
class Method:
```

Represents a method in a service\.

**Attributes:**

- **name**: str
The name of the method\.
- **input_type**: MessageType
The input type of the method\.
- **output_type**: MessageType
The output type of the method\.
- **elements**: List\[MethodElement\] = field\(default\_factory=list\)
The elements of the method\.
<a name="proto_schema_parser-ast-MessageType"></a>
### 🅲 proto\_schema\_parser\.ast\.MessageType

```python
class MessageType:
```

Represents a message type in a message\.

**Attributes:**

- **type**: str
The type of the message\.
- **stream**: bool = False
Whether the message is a stream\.
<a name="proto_schema_parser-ast-Identifier"></a>
### 🅲 proto\_schema\_parser\.ast\.Identifier

```python
class Identifier:
```

Identifier is a simple dataclass to represent an unquoted identifier \(such

as an enumerator name\)\. It's used as a value for scalar types that can't be
parsed into a string, int, float, or bool\.
<a name="proto_schema_parser-generator"></a>
## 🅼 proto\_schema\_parser\.generator

- **Classes:**
  - 🅲 [Generator](#proto_schema_parser-generator-Generator)

### Classes

<a name="proto_schema_parser-generator-Generator"></a>
### 🅲 proto\_schema\_parser\.generator\.Generator

```python
class Generator:
```

Generator class that takes an abstract syntax tree \(AST\) and

generates a protobuf schema string\.

**Functions:**

<a name="proto_schema_parser-generator-Generator-generate"></a>
#### 🅵 proto\_schema\_parser\.generator\.Generator\.generate

```python
def generate(self, file: ast.File) -> str:
```

Generates a protobuf schema string from an abstract syntax tree \(AST\)\.

**Parameters:**

- **file** (`ast.File`): The abstract syntax tree of the \.proto file\.

**Returns:**

- `str`: The generated protobuf schema string\.
<a name="proto_schema_parser-parser"></a>
## 🅼 proto\_schema\_parser\.parser

- **Classes:**
  - 🅲 [Parser](#proto_schema_parser-parser-Parser)

### Classes

<a name="proto_schema_parser-parser-Parser"></a>
### 🅲 proto\_schema\_parser\.parser\.Parser

```python
class Parser:
```

Parser class that takes a string representing a protobuf schema and returns an

abstract syntax tree \(AST\)\.

**Functions:**

<a name="proto_schema_parser-parser-Parser-__init__"></a>
#### 🅵 proto\_schema\_parser\.parser\.Parser\.\_\_init\_\_

```python
def __init__(self, setup_lexer: Optional[SetupLexerCb] = None, setup_parser: Optional[SetupParserCb] = None) -> None:
```

Initializes a new instance of the Parser class\.

**Parameters:**

- **setup_lexer** (`Optional[SetupLexerCb]`): A callback function to
modify the lexer during parsing\. Defaults to None\.
- **setup_parser** (`Optional[SetupParserCb]`): A callback function
to modify the parser during parsing\. Defaults to None\.
<a name="proto_schema_parser-parser-Parser-parse"></a>
#### 🅵 proto\_schema\_parser\.parser\.Parser\.parse

```python
def parse(self, text: str) -> ast.File:
```

Parses a string representing a protobuf schema and returns an abstract syntax tree \(AST\)\.

**Parameters:**

- **text** (`str`): The string representing the protobuf schema\.

**Returns:**

- `ast.File`: The abstract syntax tree representation of the protobuf schema\.
