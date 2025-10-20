import pytest

from proto_schema_parser import ast
from proto_schema_parser.parser import Parser, _ASTConstructor


def test_parse_person():
    text = """
    // A person with a name, id, and contact info
    message Person {
      // Includes both first and last name
      required string name = 1;
      required int32 id = 2;
      /* Email address
       * Note: only one or zero is supported
       */
      optional string email = 3;

      enum PhoneType {
        MOBILE = 0;
        HOME = 1;
        WORK = 2;
      }

      message PhoneNumber {
        optional string number = 1;
        optional PhoneType type = 2 [default = HOME];
      }

      repeated PhoneNumber phones = 4;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax=None,
        file_elements=[
            ast.Comment(text="// A person with a name, id, and contact info"),
            ast.Message(
                name="Person",
                elements=[
                    ast.Comment(text="// Includes both first and last name"),
                    ast.Field(
                        name="name",
                        number=1,
                        cardinality=ast.FieldCardinality.REQUIRED,
                        type="string",
                        options=[],
                    ),
                    ast.Field(
                        name="id",
                        number=2,
                        cardinality=ast.FieldCardinality.REQUIRED,
                        type="int32",
                        options=[],
                    ),
                    ast.Comment(
                        text="/* Email address\n       * Note: only one or zero is supported\n       */"
                    ),
                    ast.Field(
                        name="email",
                        number=3,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        type="string",
                        options=[],
                    ),
                    ast.Enum(
                        name="PhoneType",
                        elements=[
                            ast.EnumValue(
                                name="MOBILE",
                                number=0,
                                options=[],
                            ),
                            ast.EnumValue(
                                name="HOME",
                                number=1,
                                options=[],
                            ),
                            ast.EnumValue(
                                name="WORK",
                                number=2,
                                options=[],
                            ),
                        ],
                    ),
                    ast.Message(
                        name="PhoneNumber",
                        elements=[
                            ast.Field(
                                name="number",
                                number=1,
                                cardinality=ast.FieldCardinality.OPTIONAL,
                                type="string",
                                options=[],
                            ),
                            ast.Field(
                                name="type",
                                number=2,
                                cardinality=ast.FieldCardinality.OPTIONAL,
                                type="PhoneType",
                                options=[
                                    ast.Option(
                                        name="default", value=ast.Identifier("HOME")
                                    )
                                ],
                            ),
                        ],
                    ),
                    ast.Field(
                        name="phones",
                        number=4,
                        cardinality=ast.FieldCardinality.REPEATED,
                        type="PhoneNumber",
                        options=[],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_search_request():
    text = """
    syntax = "proto3";

    message SearchRequest {
      string query = 1 [(validate.rules).double = {gte: -90,  lte: 90}];
      optional int32 page_number = 2;
      option foo = "bar";
      int32 results_per_page = 3;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="SearchRequest",
                elements=[
                    ast.Field(
                        name="query",
                        number=1,
                        type="string",
                        # AST doesn't include white space
                        options=[
                            ast.Option(
                                name="(validate.rules).double",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(name="gte", value=-90),
                                        ast.MessageLiteralField(name="lte", value=90),
                                    ]
                                ),
                            )
                        ],
                    ),
                    ast.Field(
                        name="page_number",
                        number=2,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        type="int32",
                        options=[],
                    ),
                    ast.Option(name="foo", value="bar"),
                    ast.Field(
                        name="results_per_page",
                        number=3,
                        type="int32",
                        options=[],
                    ),
                ],
            )
        ],
    )
    assert result == expected


def test_parse_foo():
    text = """
    syntax = "proto3";

    message Foo {
      message Bar {
        required string name = 1;
        required string value = 2;
      }

      message Baz {
        required Bar a = 1;
      }

      optional Baz baz = 1;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="Foo",
                elements=[
                    ast.Message(
                        name="Bar",
                        elements=[
                            ast.Field(
                                name="name",
                                number=1,
                                cardinality=ast.FieldCardinality.REQUIRED,
                                type="string",
                                options=[],
                            ),
                            ast.Field(
                                name="value",
                                number=2,
                                cardinality=ast.FieldCardinality.REQUIRED,
                                type="string",
                                options=[],
                            ),
                        ],
                    ),
                    ast.Message(
                        name="Baz",
                        elements=[
                            ast.Field(
                                name="a",
                                number=1,
                                cardinality=ast.FieldCardinality.REQUIRED,
                                type="Bar",
                                options=[],
                            ),
                        ],
                    ),
                    ast.Field(
                        name="baz",
                        number=1,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        type="Baz",
                        options=[],
                    ),
                ],
            )
        ],
    )
    assert result == expected


def test_parse_oneof():
    text = """
    syntax = "proto3";

    message SampleMessage {
      oneof test_oneof {
        string name = 1;
        int32 id = 2;
        bool active = 3;
      }
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="SampleMessage",
                elements=[
                    ast.OneOf(
                        name="test_oneof",
                        elements=[
                            ast.Field(
                                name="name",
                                number=1,
                                type="string",
                                options=[],
                            ),
                            ast.Field(
                                name="id",
                                number=2,
                                type="int32",
                                options=[],
                            ),
                            ast.Field(
                                name="active",
                                number=3,
                                type="bool",
                                options=[],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
    assert result == expected


def test_parse_map():
    text = """
    syntax = "proto3";

    message SampleMap {
      map<string, int32> test_map = 1;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="SampleMap",
                elements=[
                    ast.MapField(
                        name="test_map",
                        number=1,
                        key_type="string",
                        value_type="int32",
                        options=[],
                    ),
                ],
            )
        ],
    )
    assert result == expected


def test_parse_group():
    text = """
    syntax = "proto2";

    message SearchResponse {
      repeated group Result = 1 {
        required string url = 2;
        optional string title = 3;
        repeated string snippets = 4;
      }
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto2",
        file_elements=[
            ast.Message(
                name="SearchResponse",
                elements=[
                    ast.Group(
                        name="Result",
                        number=1,
                        cardinality=ast.FieldCardinality.REPEATED,
                        elements=[
                            ast.Field(
                                name="url",
                                number=2,
                                cardinality=ast.FieldCardinality.REQUIRED,
                                type="string",
                                options=[],
                            ),
                            ast.Field(
                                name="title",
                                number=3,
                                cardinality=ast.FieldCardinality.OPTIONAL,
                                type="string",
                                options=[],
                            ),
                            ast.Field(
                                name="snippets",
                                number=4,
                                cardinality=ast.FieldCardinality.REPEATED,
                                type="string",
                                options=[],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
    assert result == expected


def test_parse_extension():
    text = """
    syntax = "proto2";

    message Foo {
      extensions 100 to max;
    }

    extend Foo {
      optional int32 bar = 101;
    }

    extend Foo_Comment {
      // This is a comment.
      optional int32 bar = 101;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto2",
        file_elements=[
            ast.Message(
                name="Foo",
                elements=[
                    ast.ExtensionRange(
                        ranges=["100 to max"],
                    ),
                ],
            ),
            ast.Extension(
                typeName="Foo",
                elements=[
                    ast.Field(
                        name="bar",
                        number=101,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        type="int32",
                        options=[],
                    ),
                ],
            ),
            ast.Extension(
                typeName="Foo_Comment",
                elements=[
                    ast.Comment(text="// This is a comment."),
                    ast.Field(
                        name="bar",
                        number=101,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        type="int32",
                        options=[],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_option_extension_with_message():
    text = """
    syntax = "proto3";
    package test.options.v1;

    message Version
    {
        required uint32 major = 1;
        required uint32 minor = 2;
    }

    message ServiceOptions {
        extensions 1000 to max;
    }

    extend ServiceOptions
    {
        Version version = 1001;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Package(
                name="test.options.v1",
            ),
            ast.Message(
                name="Version",
                elements=[
                    ast.Field(
                        name="major",
                        number=1,
                        type="uint32",
                        cardinality=ast.FieldCardinality.REQUIRED,
                        options=[],
                    ),
                    ast.Field(
                        name="minor",
                        number=2,
                        type="uint32",
                        cardinality=ast.FieldCardinality.REQUIRED,
                        options=[],
                    ),
                ],
            ),
            ast.Message(
                name="ServiceOptions",
                elements=[
                    ast.ExtensionRange(
                        ranges=[
                            "1000 to max",
                        ],
                        options=[],
                    ),
                ],
            ),
            ast.Extension(
                typeName="ServiceOptions",
                elements=[
                    ast.Field(
                        name="version",
                        number=1001,
                        cardinality=None,
                        type="Version",
                        options=[],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_imports():
    text = """
    syntax = "proto3";

    import "other/file.proto";
    import public "public/file.proto";
    import weak "weak/file.proto";
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Import(
                name="other/file.proto",
            ),
            ast.Import(
                name="public/file.proto",
                public=True,
            ),
            ast.Import(
                name="weak/file.proto",
                weak=True,
            ),
        ],
    )
    assert result == expected


def test_parse_package():
    text = """
    syntax = "proto3";

    package foo.bar;
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Package(
                name="foo.bar",
            ),
        ],
    )
    assert result == expected


def test_parse_reserved():
    text = """
    syntax = "proto3";

    message Foo {
      reserved 2, 15, 9 to 11;
      reserved "foo", "bar";
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="Foo",
                elements=[
                    ast.Reserved(ranges=["2", "15", "9 to 11"]),
                    ast.Reserved(names=["foo", "bar"]),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_enum_reserved():
    text = """
    syntax = "proto3";

    enum Foo {
      BAR = 0;
      BAZ = 1;
      reserved 2, 3, 4 to 8;
      reserved "QUX", "QUUX";
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Enum(
                name="Foo",
                elements=[
                    ast.EnumValue(
                        name="BAR",
                        number=0,
                        options=[],
                    ),
                    ast.EnumValue(
                        name="BAZ",
                        number=1,
                        options=[],
                    ),
                    ast.EnumReserved(
                        ranges=["2", "3", "4 to 8"],
                    ),
                    ast.EnumReserved(
                        names=["QUX", "QUUX"],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_message_option():
    text = """
    syntax = "proto3";

    message Foo {
      option deprecated = true;
      option some_num = 123;
      option some_float = 123.3;
      string name = 1;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="Foo",
                elements=[
                    ast.Option(
                        name="deprecated",
                        value=True,
                    ),
                    ast.Option(
                        name="some_num",
                        value=123,
                    ),
                    ast.Option(
                        name="some_float",
                        value=123.3,
                    ),
                    ast.Field(
                        name="name",
                        number=1,
                        type="string",
                        options=[],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_oneof_option():
    text = """
    syntax = "proto3";

    message SampleMessage {
        oneof test_oneof {
            option (my_option) = "example";
            string name = 1;
            int32 id = 2;
        }
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="SampleMessage",
                elements=[
                    ast.OneOf(
                        name="test_oneof",
                        elements=[
                            ast.Option(name="(my_option)", value="example"),
                            ast.Field(
                                name="name",
                                number=1,
                                type="string",
                                options=[],
                            ),
                            ast.Field(
                                name="id",
                                number=2,
                                type="int32",
                                options=[],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
    assert result == expected


def test_parse_enum_option():
    text = """
    syntax = "proto3";

    enum SampleEnum {
        option (my_option) = "example";
        UNKNOWN = 0;
        STARTED = 1;
        RUNNING = 2;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Enum(
                name="SampleEnum",
                elements=[
                    ast.Option(name="(my_option)", value="example"),
                    ast.EnumValue(
                        name="UNKNOWN",
                        number=0,
                        options=[],
                    ),
                    ast.EnumValue(
                        name="STARTED",
                        number=1,
                        options=[],
                    ),
                    ast.EnumValue(
                        name="RUNNING",
                        number=2,
                        options=[],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_oneof_group():
    text = """
    syntax = "proto2";

    message SampleMessage {
        oneof test_oneof {
            group NameGroup = 1 {
                required string name = 2;
            }
            int32 id = 3;
        }
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto2",
        file_elements=[
            ast.Message(
                name="SampleMessage",
                elements=[
                    ast.OneOf(
                        name="test_oneof",
                        elements=[
                            ast.Group(
                                name="NameGroup",
                                number=1,
                                elements=[
                                    ast.Field(
                                        name="name",
                                        number=2,
                                        cardinality=ast.FieldCardinality.REQUIRED,
                                        type="string",
                                        options=[],
                                    ),
                                ],
                            ),
                            ast.Field(
                                name="id",
                                number=3,
                                type="int32",
                                options=[],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
    assert result == expected


def test_parse_extend_group():
    text = """
    syntax = "proto2";

    message SampleMessage {
        extensions 100 to 200;
    }

    extend SampleMessage {
        group ExtendGroup = 100 {
            required string name = 2;
        }
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto2",
        file_elements=[
            ast.Message(
                name="SampleMessage",
                elements=[
                    ast.ExtensionRange(ranges=["100 to 200"], options=[]),
                ],
            ),
            ast.Extension(
                typeName="SampleMessage",
                elements=[
                    ast.Group(
                        name="ExtendGroup",
                        number=100,
                        elements=[
                            ast.Field(
                                name="name",
                                number=2,
                                cardinality=ast.FieldCardinality.REQUIRED,
                                type="string",
                                options=[],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_service():
    text = """
    syntax = "proto3";

    service ExampleService {
        rpc UnaryCall (ExampleRequest) returns (ExampleResponse);
        rpc StreamingFromServer (ExampleRequest) returns (stream ExampleResponse);
        rpc StreamingFromClient (stream ExampleRequest) returns (ExampleResponse);
        option (my_service_option) = FOO;
        rpc MyMethod(RequestType) returns(ResponseType) {
            option (my_method_option).foo = 567;
            option (my_method_option).bar = "Some string";
        }
        rpc MyMethod_Semicolon(RequestType) returns(ResponseType) {
            option (my_method_option).foo = 567;
            option (my_method_option).bar = "Some string";
        };
    }

    service ExampleEmptyService {}
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Service(
                name="ExampleService",
                elements=[
                    ast.Method(
                        name="UnaryCall",
                        input_type=ast.MessageType(type="ExampleRequest"),
                        output_type=ast.MessageType(type="ExampleResponse"),
                    ),
                    ast.Method(
                        name="StreamingFromServer",
                        input_type=ast.MessageType(type="ExampleRequest"),
                        output_type=ast.MessageType(
                            type="ExampleResponse", stream=True
                        ),
                    ),
                    ast.Method(
                        name="StreamingFromClient",
                        input_type=ast.MessageType(type="ExampleRequest", stream=True),
                        output_type=ast.MessageType(type="ExampleResponse"),
                    ),
                    ast.Option(name="(my_service_option)", value=ast.Identifier("FOO")),
                    ast.Method(
                        name="MyMethod",
                        input_type=ast.MessageType(type="RequestType"),
                        output_type=ast.MessageType(type="ResponseType"),
                        elements=[
                            ast.Option(name="(my_method_option).foo", value=567),
                            ast.Option(
                                name="(my_method_option).bar", value="Some string"
                            ),
                        ],
                    ),
                    ast.Method(
                        name="MyMethod_Semicolon",
                        input_type=ast.MessageType(type="RequestType"),
                        output_type=ast.MessageType(type="ResponseType"),
                        elements=[
                            ast.Option(name="(my_method_option).foo", value=567),
                            ast.Option(
                                name="(my_method_option).bar", value="Some string"
                            ),
                        ],
                    ),
                ],
            ),
            ast.Service(
                name="ExampleEmptyService",
                elements=[],
            ),
        ],
    )
    assert result == expected


def test_parse_comments_in_enum():
    test = """
    syntax = "proto3";

    enum SampleEnum {
        // This is a comment
        UNKNOWN = 0;
        SOMETHING = 1; // comment on same line
        ELSE = 2;
        // trailing comment
        MORE = 3;
        /* multi-line
        comment
        */
    }
    """

    result = Parser().parse(test)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Enum(
                name="SampleEnum",
                elements=[
                    ast.Comment(text="// This is a comment"),
                    ast.EnumValue(
                        name="UNKNOWN",
                        number=0,
                        options=[],
                    ),
                    ast.EnumValue(
                        name="SOMETHING",
                        number=1,
                        options=[],
                    ),
                    ast.Comment(text="// comment on same line", inline=True),
                    ast.EnumValue(
                        name="ELSE",
                        number=2,
                        options=[],
                    ),
                    ast.Comment(text="// trailing comment"),
                    ast.EnumValue(
                        name="MORE",
                        number=3,
                        options=[],
                    ),
                    ast.Comment(text="/* multi-line\n        comment\n        */"),
                ],
            ),
        ],
    )

    assert result == expected


def test_parse_comments_in_oneofs():
    test = """
    syntax = "proto3";
    message TestMessage {
        oneof test_oneof {
            // This is a comment
            string name = 1;
            int32 id = 2; // comment on same line
            // trailing comment
            bool active = 3;
            /* multi-line
            comment
            */
        }
    }
    """

    result = Parser().parse(test)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="TestMessage",
                elements=[
                    ast.OneOf(
                        name="test_oneof",
                        elements=[
                            ast.Comment(text="// This is a comment"),
                            ast.Field(
                                name="name",
                                number=1,
                                type="string",
                                options=[],
                            ),
                            ast.Field(
                                name="id",
                                number=2,
                                type="int32",
                                options=[],
                            ),
                            ast.Comment(text="// comment on same line", inline=True),
                            ast.Comment(text="// trailing comment"),
                            ast.Field(
                                name="active",
                                number=3,
                                type="bool",
                                options=[],
                            ),
                            ast.Comment(
                                text="/* multi-line\n            comment\n            */"
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    assert result == expected


def test_parse_comments_in_service():
    text = """
    syntax = "proto3";

    service ExampleService {
        // This is a comment
        rpc UnaryCall (ExampleRequest) returns (ExampleResponse) { }
        rpc StreamingFromServer (ExampleRequest) returns (stream ExampleResponse); // comment on same line
        // trailing comment
        rpc StreamingFromClient (stream ExampleRequest) returns (ExampleResponse) {
            // comment in RPC
            option (my_method_option).foo = 567; // comment in RPC on same line
            /* multi-line
            comment
            in RPC */
        }
        /* multi-line
        comment
        */
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Service(
                name="ExampleService",
                elements=[
                    ast.Comment(text="// This is a comment"),
                    ast.Method(
                        name="UnaryCall",
                        input_type=ast.MessageType(type="ExampleRequest"),
                        output_type=ast.MessageType(type="ExampleResponse"),
                    ),
                    ast.Method(
                        name="StreamingFromServer",
                        input_type=ast.MessageType(type="ExampleRequest"),
                        output_type=ast.MessageType(
                            type="ExampleResponse", stream=True
                        ),
                    ),
                    ast.Comment(text="// comment on same line", inline=True),
                    ast.Comment(text="// trailing comment"),
                    ast.Method(
                        name="StreamingFromClient",
                        input_type=ast.MessageType(type="ExampleRequest", stream=True),
                        output_type=ast.MessageType(type="ExampleResponse"),
                        elements=[
                            ast.Comment(text="// comment in RPC"),
                            ast.Option(name="(my_method_option).foo", value=567),
                            ast.Comment(
                                text="// comment in RPC on same line", inline=True
                            ),
                            ast.Comment(
                                text="/* multi-line\n            comment\n            in RPC */"
                            ),
                        ],
                    ),
                    ast.Comment(text="/* multi-line\n        comment\n        */"),
                ],
            ),
        ],
    )

    assert result == expected


def test_comments_at_beginning_of_file():
    text = """
    // This is a comment
    syntax = "proto3";

    message ExampleMessage {
        // Field comment
        string example_field = 1;
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Comment(text="// This is a comment"),
            ast.Message(
                name="ExampleMessage",
                elements=[
                    ast.Comment(text="// Field comment"),
                    ast.Field(
                        name="example_field",
                        number=1,
                        type="string",
                        options=[],
                    ),
                ],
            ),
        ],
    )

    assert result == expected


def test_enum_with_hex_value():
    text = """
    syntax = "proto3";

    enum SampleEnum {
        UNKNOWN = 0;
        SOMETHING = 0xC8;
        ELSE = 2;
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Enum(
                name="SampleEnum",
                elements=[
                    ast.EnumValue(
                        name="UNKNOWN",
                        number=0,
                        options=[],
                    ),
                    ast.EnumValue(
                        name="SOMETHING",
                        number=200,
                        options=[],
                    ),
                    ast.EnumValue(
                        name="ELSE",
                        number=2,
                        options=[],
                    ),
                ],
            ),
        ],
    )

    assert result == expected


def test_comments_on_service_and_options():
    text = """
    syntax = "proto3";

    message SearchRequest {
        string query = 1;
    }

    service SearchService {
        // Do the search
        rpc Search(SearchRequest) returns (SearchResponse) {
            option (google.api.http) = {
                // some comment about the option
                get: "/v1/search/{query}"
            };
        }
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="SearchRequest",
                elements=[
                    ast.Field(
                        name="query",
                        number=1,
                        type="string",
                        options=[],
                    ),
                ],
            ),
            ast.Service(
                name="SearchService",
                elements=[
                    ast.Comment(text="// Do the search"),
                    ast.Method(
                        name="Search",
                        input_type=ast.MessageType(type="SearchRequest"),
                        output_type=ast.MessageType(type="SearchResponse"),
                        elements=[
                            ast.Option(
                                name="(google.api.http)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.Comment(
                                            text="// some comment about the option"
                                        ),
                                        ast.MessageLiteralField(
                                            name="get",
                                            value="/v1/search/{query}",
                                        ),
                                    ]
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    assert result == expected


def test_trailing_comments_exhaustive_complex_schema_parser():
    """
    Exhaustive trailing-comment validation across a very complex schema.

    This test verifies the exact AST structure including all comments in their
    proper positions throughout the protobuf file.
    """

    schema = """
syntax = "proto2"; // TC#1 syntax
package very.complex.schema.v1; // TC#2 package

import "google/protobuf/descriptor.proto"; // TC#3 import1
import public "company/common.proto"; // TC#4 import public
import weak "company/weak.proto"; // TC#5 import weak

option (company.file_opt).enabled = true; // TC#6 file option bool
option java_package = "com.company.schema"; // TC#7 file option string
option (company.file_opt_msg) = { // TC#8 option msg begin
  inner: { // TC#9 inner begin
    a: 1, // TC#10 inner field a
    b: [1, 2, 3], // TC#11 inner field b list
    c: { x: "y" } // TC#12 inner inline message
  }, // TC#13 inner end with comma
  list_of_msgs: { i: 1 }, // TC#14 list of messages
  list_of_msgs: { i: 2 }
}; // TC#15 option msg end

message Outer { // TC#16 message open
  option deprecated = true; // TC#17 message option
  required string name = 1; // TC#18 field required
  optional int32 id = 2; // TC#19 fixed: packed only valid on repeated
  map<string, int64> attrs = 3; // TC#20 map field
  required group InnerGroup = 4 { // TC#21 group open
    optional bool flag = 1; // TC#22 group field
  } // TC#23 group close
  oneof choice { // TC#24 oneof open
    string a = 5; // TC#25 oneof field a
    G g = 6; // TC#26 fixed: groups are not allowed in oneof
  } // TC#29 oneof close
  extensions 100 to 199, 500 to max; // TC#30 extensions
  reserved 8, 9 to 11; // TC#31 reserved ranges
  reserved "foo", "bar"; // TC#31b reserved names

  // Replacement for the oneof group
  message G {
    optional int32 v = 1; // TC#27 oneof group field
  }

  message Nested { // TC#32 nested message open
    optional bytes data = 1; // TC#33 nested field
  } // TC#34 nested message close
  enum Status { // TC#35 enum open
    UNKNOWN = 0; // TC#36 enum value
    READY = 1; // TC#37 enum value
    reserved 2 to 4; // TC#38 enum reserved range
    reserved "OLD"; // TC#38b enum reserved name
  } // TC#39 enum close
} // TC#40 message close

extend Outer { // TC#41 extension decl open
  optional string ext_f = 1000; // TC#42 extension field
  optional group ExtG = 1001 { // TC#43 fixed: add label
    int32 ev = 1; // TC#44 extension group field
  } // TC#45 extension group close
} // TC#46 extension decl close

service Svc { // TC#47 service open
  option (company.svc_opt) = { // TC#48 service option open
    get: "/v1/x", // TC#49 service opt field get
    additional_bindings { // TC#50 nested msg literal open
      post: "/v1/y" // TC#51 nested field post
    } // TC#52 nested msg literal close
  }; // TC#53 service option close
  rpc Unary (Outer) returns (Outer.Nested); // TC#54 fixed: qualify Nested
  rpc Bidi (stream Outer) returns (stream Outer) { // TC#55 rpc block open
    option (company.mtd_opt).num = 7; // TC#56 method option
  } // TC#57 rpc block close
} // TC#58 service close
"""

    result = Parser().parse(schema)

    expected = ast.File(
        syntax="proto2",
        file_elements=[
            ast.Comment(text="// TC#1 syntax", inline=True),
            ast.Package(name="very.complex.schema.v1"),
            ast.Comment(text="// TC#2 package", inline=True),
            ast.Import(name="google/protobuf/descriptor.proto"),
            ast.Comment(text="// TC#3 import1", inline=True),
            ast.Import(name="company/common.proto", public=True),
            ast.Comment(text="// TC#4 import public", inline=True),
            ast.Import(name="company/weak.proto", weak=True),
            ast.Comment(text="// TC#5 import weak", inline=True),
            ast.Option(
                name="(company.file_opt).enabled",
                value=True,
            ),
            ast.Comment(text="// TC#6 file option bool", inline=True),
            ast.Option(
                name="java_package",
                value="com.company.schema",
            ),
            ast.Comment(text="// TC#7 file option string", inline=True),
            ast.Option(
                name="(company.file_opt_msg)",
                value=ast.MessageLiteral(
                    elements=[
                        ast.Comment(text="// TC#8 option msg begin", inline=True),
                        ast.MessageLiteralField(
                            name="inner",
                            value=ast.MessageLiteral(
                                elements=[
                                    ast.Comment(
                                        text="// TC#9 inner begin", inline=True
                                    ),
                                    ast.MessageLiteralField(name="a", value=1),
                                    ast.Comment(
                                        text="// TC#10 inner field a", inline=True
                                    ),
                                    ast.MessageLiteralField(name="b", value=[1, 2, 3]),
                                    ast.Comment(
                                        text="// TC#11 inner field b list", inline=True
                                    ),
                                    ast.MessageLiteralField(
                                        name="c",
                                        value=ast.MessageLiteral(
                                            elements=[
                                                ast.MessageLiteralField(
                                                    name="x", value="y"
                                                ),
                                            ]
                                        ),
                                    ),
                                    ast.Comment(
                                        text="// TC#12 inner inline message",
                                        inline=True,
                                    ),
                                ]
                            ),
                        ),
                        ast.Comment(text="// TC#13 inner end with comma", inline=True),
                        ast.MessageLiteralField(
                            name="list_of_msgs",
                            value=ast.MessageLiteral(
                                elements=[
                                    ast.MessageLiteralField(name="i", value=1),
                                ]
                            ),
                        ),
                        ast.Comment(text="// TC#14 list of messages", inline=True),
                        ast.MessageLiteralField(
                            name="list_of_msgs",
                            value=ast.MessageLiteral(
                                elements=[
                                    ast.MessageLiteralField(name="i", value=2),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            ast.Comment(text="// TC#15 option msg end", inline=True),
            ast.Message(
                name="Outer",
                elements=[
                    ast.Comment(text="// TC#16 message open", inline=True),
                    ast.Option(name="deprecated", value=True),
                    ast.Comment(text="// TC#17 message option", inline=True),
                    ast.Field(
                        name="name",
                        number=1,
                        type="string",
                        cardinality=ast.FieldCardinality.REQUIRED,
                        options=[],
                    ),
                    ast.Comment(text="// TC#18 field required", inline=True),
                    ast.Field(
                        name="id",
                        number=2,
                        type="int32",
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        options=[],
                    ),
                    ast.Comment(
                        text="// TC#19 fixed: packed only valid on repeated",
                        inline=True,
                    ),
                    ast.MapField(
                        name="attrs",
                        number=3,
                        key_type="string",
                        value_type="int64",
                        options=[],
                    ),
                    ast.Comment(text="// TC#20 map field", inline=True),
                    ast.Group(
                        name="InnerGroup",
                        number=4,
                        cardinality=ast.FieldCardinality.REQUIRED,
                        elements=[
                            ast.Comment(text="// TC#21 group open", inline=True),
                            ast.Field(
                                name="flag",
                                number=1,
                                type="bool",
                                cardinality=ast.FieldCardinality.OPTIONAL,
                                options=[],
                            ),
                            ast.Comment(text="// TC#22 group field", inline=True),
                        ],
                    ),
                    ast.Comment(text="// TC#23 group close", inline=True),
                    ast.OneOf(
                        name="choice",
                        elements=[
                            ast.Comment(text="// TC#24 oneof open", inline=True),
                            ast.Field(
                                name="a",
                                number=5,
                                type="string",
                                options=[],
                            ),
                            ast.Comment(text="// TC#25 oneof field a", inline=True),
                            ast.Field(
                                name="g",
                                number=6,
                                type="G",
                                options=[],
                            ),
                            ast.Comment(
                                text="// TC#26 fixed: groups are not allowed in oneof",
                                inline=True,
                            ),
                        ],
                    ),
                    ast.Comment(text="// TC#29 oneof close", inline=True),
                    ast.ExtensionRange(
                        ranges=["100 to 199", "500 to max"],
                        options=[],
                    ),
                    ast.Comment(text="// TC#30 extensions", inline=True),
                    ast.Reserved(
                        ranges=["8", "9 to 11"],
                    ),
                    ast.Comment(text="// TC#31 reserved ranges", inline=True),
                    ast.Reserved(
                        names=["foo", "bar"],
                    ),
                    ast.Comment(text="// TC#31b reserved names", inline=True),
                    ast.Comment(text="// Replacement for the oneof group"),
                    ast.Message(
                        name="G",
                        elements=[
                            ast.Field(
                                name="v",
                                number=1,
                                type="int32",
                                cardinality=ast.FieldCardinality.OPTIONAL,
                                options=[],
                            ),
                            ast.Comment(text="// TC#27 oneof group field", inline=True),
                        ],
                    ),
                    ast.Message(
                        name="Nested",
                        elements=[
                            ast.Comment(
                                text="// TC#32 nested message open", inline=True
                            ),
                            ast.Field(
                                name="data",
                                number=1,
                                type="bytes",
                                cardinality=ast.FieldCardinality.OPTIONAL,
                                options=[],
                            ),
                            ast.Comment(text="// TC#33 nested field", inline=True),
                        ],
                    ),
                    ast.Comment(text="// TC#34 nested message close", inline=True),
                    ast.Enum(
                        name="Status",
                        elements=[
                            ast.Comment(text="// TC#35 enum open", inline=True),
                            ast.EnumValue(
                                name="UNKNOWN",
                                number=0,
                                options=[],
                            ),
                            ast.Comment(text="// TC#36 enum value", inline=True),
                            ast.EnumValue(
                                name="READY",
                                number=1,
                                options=[],
                            ),
                            ast.Comment(text="// TC#37 enum value", inline=True),
                            ast.EnumReserved(
                                ranges=["2 to 4"],
                            ),
                            ast.Comment(
                                text="// TC#38 enum reserved range", inline=True
                            ),
                            ast.EnumReserved(
                                names=["OLD"],
                            ),
                            ast.Comment(
                                text="// TC#38b enum reserved name", inline=True
                            ),
                        ],
                    ),
                    ast.Comment(text="// TC#39 enum close", inline=True),
                ],
            ),
            ast.Comment(text="// TC#40 message close", inline=True),
            ast.Extension(
                typeName="Outer",
                elements=[
                    ast.Comment(text="// TC#41 extension decl open", inline=True),
                    ast.Field(
                        name="ext_f",
                        number=1000,
                        type="string",
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        options=[],
                    ),
                    ast.Comment(text="// TC#42 extension field", inline=True),
                    ast.Group(
                        name="ExtG",
                        number=1001,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        elements=[
                            ast.Comment(text="// TC#43 fixed: add label", inline=True),
                            ast.Field(
                                name="ev",
                                number=1,
                                type="int32",
                                options=[],
                            ),
                            ast.Comment(
                                text="// TC#44 extension group field", inline=True
                            ),
                        ],
                    ),
                    ast.Comment(text="// TC#45 extension group close", inline=True),
                ],
            ),
            ast.Comment(text="// TC#46 extension decl close", inline=True),
            ast.Service(
                name="Svc",
                elements=[
                    ast.Comment(text="// TC#47 service open", inline=True),
                    ast.Option(
                        name="(company.svc_opt)",
                        value=ast.MessageLiteral(
                            elements=[
                                ast.Comment(
                                    text="// TC#48 service option open", inline=True
                                ),
                                ast.MessageLiteralField(name="get", value="/v1/x"),
                                ast.Comment(
                                    text="// TC#49 service opt field get", inline=True
                                ),
                                ast.MessageLiteralField(
                                    name="additional_bindings",
                                    value=ast.MessageLiteral(
                                        elements=[
                                            ast.Comment(
                                                text="// TC#50 nested msg literal open",
                                                inline=True,
                                            ),
                                            ast.MessageLiteralField(
                                                name="post", value="/v1/y"
                                            ),
                                            ast.Comment(
                                                text="// TC#51 nested field post",
                                                inline=True,
                                            ),
                                        ]
                                    ),
                                ),
                                ast.Comment(
                                    text="// TC#52 nested msg literal close",
                                    inline=True,
                                ),
                            ]
                        ),
                    ),
                    ast.Comment(text="// TC#53 service option close", inline=True),
                    ast.Method(
                        name="Unary",
                        input_type=ast.MessageType(type="Outer"),
                        output_type=ast.MessageType(type="Outer.Nested"),
                        elements=[],
                    ),
                    ast.Comment(text="// TC#54 fixed: qualify Nested", inline=True),
                    ast.Method(
                        name="Bidi",
                        input_type=ast.MessageType(type="Outer", stream=True),
                        output_type=ast.MessageType(type="Outer", stream=True),
                        elements=[
                            ast.Comment(text="// TC#55 rpc block open", inline=True),
                            ast.Option(name="(company.mtd_opt).num", value=7),
                            ast.Comment(text="// TC#56 method option", inline=True),
                        ],
                    ),
                    ast.Comment(text="// TC#57 rpc block close", inline=True),
                ],
            ),
            ast.Comment(text="// TC#58 service close", inline=True),
        ],
    )

    assert result == expected


def test_comment_with_trailing_quote():
    text = """
    syntax = "proto3";

    message ExampleMessage {
        // This is a comment with a trailing quote"
        string example_field = 1;
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="ExampleMessage",
                elements=[
                    ast.Comment(text='// This is a comment with a trailing quote"'),
                    ast.Field(
                        name="example_field",
                        number=1,
                        type="string",
                        options=[],
                    ),
                ],
            ),
        ],
    )

    assert result == expected


def test_parse_message_literal_with_braces():
    text = """
    syntax = "proto3";

    message SearchRequest {
        option (custom_option) = {
            field1: "value1",
            field2: 42,
            nested_field: {
                key1: "nested_value1",
                key2: [1, 2, 3]
            }
        };
        string query = 1;
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="SearchRequest",
                elements=[
                    ast.Option(
                        name="(custom_option)",
                        value=ast.MessageLiteral(
                            elements=[
                                ast.MessageLiteralField(name="field1", value="value1"),
                                ast.MessageLiteralField(name="field2", value=42),
                                ast.MessageLiteralField(
                                    name="nested_field",
                                    value=ast.MessageLiteral(
                                        elements=[
                                            ast.MessageLiteralField(
                                                name="key1", value="nested_value1"
                                            ),
                                            ast.MessageLiteralField(
                                                name="key2", value=[1, 2, 3]
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ast.Field(
                        name="query",
                        number=1,
                        type="string",
                        options=[],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_nested_empty_message_literal_option():
    text = """
    message FieldAttr {
      message Nested {
        string text = 1;
      }

      Nested nested = 1;
    }

    message FieldAttributes {
      optional FieldAttr attr = 1;
    }

    extend google.protobuf.FieldOptions {
      optional FieldAttributes field_attributes = 50001;
    }

    message MyMessage {
      string title = 1 [
        (field_attributes).attr = { nested: {} },
      ];
    }
    """

    file = Parser().parse(text)

    my_message = next(
        element
        for element in file.file_elements
        if isinstance(element, ast.Message) and element.name == "MyMessage"
    )

    title_field = next(
        element
        for element in my_message.elements
        if isinstance(element, ast.Field) and element.name == "title"
    )

    option = title_field.options[0]
    assert isinstance(option.value, ast.MessageLiteral)

    nested_field = option.value.elements[0]
    assert isinstance(nested_field, ast.MessageLiteralField)
    assert nested_field.name == "nested"
    assert isinstance(nested_field.value, ast.MessageLiteral)
    assert nested_field.value.elements == []


def test_option_with_scalar_values():
    text = """
    syntax = "proto3";

    service TestService {
        rpc TestMethod (TestRequest) returns (TestResponse) {
            option (test.option) = { int_field: 123 };
            option (test.option) = { float_field: 45.67 };
            option (test.option) = { bool_field: true };
            option (test.option) = { string_field: "Hello" };
        }
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Service(
                name="TestService",
                elements=[
                    ast.Method(
                        name="TestMethod",
                        input_type=ast.MessageType(type="TestRequest"),
                        output_type=ast.MessageType(type="TestResponse"),
                        elements=[
                            ast.Option(
                                name="(test.option)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="int_field", value=123
                                        )
                                    ]
                                ),
                            ),
                            ast.Option(
                                name="(test.option)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="float_field", value=45.67
                                        )
                                    ]
                                ),
                            ),
                            ast.Option(
                                name="(test.option)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="bool_field", value=True
                                        )
                                    ]
                                ),
                            ),
                            ast.Option(
                                name="(test.option)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="string_field", value="Hello"
                                        )
                                    ]
                                ),
                            ),
                        ],
                    )
                ],
            )
        ],
    )

    assert result == expected


def test_option_with_nested_message_literal():
    text = """
    syntax = "proto3";

    service NestedService {
        rpc NestedMethod (Request) returns (Response) {
            option (test.nested) = {
                inner: { field1: "abc", field2: 42 }
            };
        }
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Service(
                name="NestedService",
                elements=[
                    ast.Method(
                        name="NestedMethod",
                        input_type=ast.MessageType(type="Request"),
                        output_type=ast.MessageType(type="Response"),
                        elements=[
                            ast.Option(
                                name="(test.nested)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="inner",
                                            value=ast.MessageLiteral(
                                                elements=[
                                                    ast.MessageLiteralField(
                                                        name="field1", value="abc"
                                                    ),
                                                    ast.MessageLiteralField(
                                                        name="field2", value=42
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )

    assert result == expected


def test_option_with_comments_and_fields():
    text = """
    syntax = "proto3";

    service CommentService {
        rpc CommentMethod (Request) returns (Response) {
            option (test.option) = {
                // Comment about the field
                field1: "value1";
                field2: 99;
                // Another comment
            };
        }
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Service(
                name="CommentService",
                elements=[
                    ast.Method(
                        name="CommentMethod",
                        input_type=ast.MessageType(type="Request"),
                        output_type=ast.MessageType(type="Response"),
                        elements=[
                            ast.Option(
                                name="(test.option)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.Comment(text="// Comment about the field"),
                                        ast.MessageLiteralField(
                                            name="field1", value="value1"
                                        ),
                                        ast.MessageLiteralField(
                                            name="field2", value=99
                                        ),
                                        ast.Comment(text="// Another comment"),
                                    ]
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )

    assert result == expected


def test_normalize_option_name_simple():
    assert _ASTConstructor.normalize_option_name("option_name") == "option_name"


def test_normalize_option_name_with_spaces():
    assert _ASTConstructor.normalize_option_name(" option . name ") == "option.name"


def test_normalize_option_name_with_parentheses():
    assert (
        _ASTConstructor.normalize_option_name(" ( option_name ) . field ")
        == "(option_name).field"
    )


def test_normalize_option_name_nested_parentheses():
    assert (
        _ASTConstructor.normalize_option_name(" ( ( nested ) . option ) . field ")
        == "(nested.option).field"
    )


def test_normalize_option_name_no_space_parentheses():
    assert (
        _ASTConstructor.normalize_option_name("(option_name).field")
        == "(option_name).field"
    )


def test_normalize_option_name_mixed_case():
    assert (
        _ASTConstructor.normalize_option_name("(Option_Name).Field")
        == "(Option_Name).Field"
    )


def test_normalize_option_name_with_extra_parentheses():
    assert (
        _ASTConstructor.normalize_option_name("( ( validate.rules ) ).double")
        == "(validate.rules).double"
    )


def test_normalize_option_name_empty():
    assert _ASTConstructor.normalize_option_name("") == ""


def test_normalize_option_name_only_parentheses():
    assert _ASTConstructor.normalize_option_name("(( ))") == "()"


def test_normalize_option_name_with_symbols():
    assert (
        _ASTConstructor.normalize_option_name("(validate.rules).$double_value")
        == "(validate.rules).$double_value"
    )


def test_parse_bool_options():
    text = """
    syntax = "proto3";

    message TestMessage {
        option (test.bool_option1) = true;
        option (test.bool_option2) = false;
        option bool_option3 = true;
        option bool_option4 = false;
        option (test.message_option) = {
            bool_field1: true,
            bool_field2: false
        };

        // Field level options
        repeated int32 packed_field = 1 [packed = true];
        repeated string unpacked_field = 2 [packed = false];
        optional bool deprecated_field = 3 [deprecated = true];
        required int64 field_with_multiple = 4 [packed = true, deprecated = false];
    }
    """
    result = Parser().parse(text)

    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="TestMessage",
                elements=[
                    ast.Option(
                        name="(test.bool_option1)",
                        value=True,
                    ),
                    ast.Option(
                        name="(test.bool_option2)",
                        value=False,
                    ),
                    ast.Option(
                        name="bool_option3",
                        value=True,
                    ),
                    ast.Option(
                        name="bool_option4",
                        value=False,
                    ),
                    ast.Option(
                        name="(test.message_option)",
                        value=ast.MessageLiteral(
                            elements=[
                                ast.MessageLiteralField(
                                    name="bool_field1",
                                    value=True,
                                ),
                                ast.MessageLiteralField(
                                    name="bool_field2",
                                    value=False,
                                ),
                            ]
                        ),
                    ),
                    ast.Comment(text="// Field level options"),
                    ast.Field(
                        name="packed_field",
                        number=1,
                        cardinality=ast.FieldCardinality.REPEATED,
                        type="int32",
                        options=[ast.Option(name="packed", value=True)],
                    ),
                    ast.Field(
                        name="unpacked_field",
                        number=2,
                        cardinality=ast.FieldCardinality.REPEATED,
                        type="string",
                        options=[ast.Option(name="packed", value=False)],
                    ),
                    ast.Field(
                        name="deprecated_field",
                        number=3,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                        type="bool",
                        options=[ast.Option(name="deprecated", value=True)],
                    ),
                    ast.Field(
                        name="field_with_multiple",
                        number=4,
                        cardinality=ast.FieldCardinality.REQUIRED,
                        type="int64",
                        options=[
                            ast.Option(name="packed", value=True),
                            ast.Option(name="deprecated", value=False),
                        ],
                    ),
                ],
            ),
        ],
    )

    assert result == expected


def test_parse_service_with_additional_bindings():
    """Test parsing a service with additional_bindings in google.api.http option."""
    text = """
    service Lease {
        rpc LeaseRevoke(LeaseRevokeRequest) returns (LeaseRevokeResponse) {
            option (google.api.http) = {
                post: "/v3/lease/revoke"
                body: "*"
                additional_bindings {
                    post: "/v3/kv/lease/revoke"
                    body: "*"
                }
            };
        }
    }
    """
    result = Parser().parse(text)
    expected = ast.File(
        syntax=None,
        file_elements=[
            ast.Service(
                name="Lease",
                elements=[
                    ast.Method(
                        name="LeaseRevoke",
                        input_type=ast.MessageType(
                            type="LeaseRevokeRequest", stream=False
                        ),
                        output_type=ast.MessageType(
                            type="LeaseRevokeResponse", stream=False
                        ),
                        elements=[
                            ast.Option(
                                name="(google.api.http)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="post", value="/v3/lease/revoke"
                                        ),
                                        ast.MessageLiteralField(name="body", value="*"),
                                        ast.MessageLiteralField(
                                            name="additional_bindings",
                                            value=ast.MessageLiteral(
                                                elements=[
                                                    ast.MessageLiteralField(
                                                        name="post",
                                                        value="/v3/kv/lease/revoke",
                                                    ),
                                                    ast.MessageLiteralField(
                                                        name="body", value="*"
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )

    assert result == expected


def test_syntax_error():
    text = """
    syntax = "proto3";

    message SearchRequest {
      string query = 1
    }
    """

    import antlr4.error.ErrorListener as antlr4_el

    import proto_schema_parser.antlr.ProtobufParser as psp_antlr

    class _ErrorListener(antlr4_el.ErrorListener):
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            raise Exception(f"Failed to parse: line {line}:{column}: {msg}")

    def _setup_parser(parser: psp_antlr.ProtobufParser) -> None:
        parser.addErrorListener(_ErrorListener())

    with pytest.raises(Exception) as exc_info:
        Parser(setup_parser=_setup_parser).parse(text)

    assert (
        exc_info.value.args[0]
        == r"Failed to parse: line 6:4: mismatched input '}' expecting {';', '['}"
    )


def test_parse_complex_compact_option():
    text_with_email = """
    syntax = "proto3";

    message Foo {
      string bar = 4 [
        (oompa.loompa) = {
          example: "mini@mouse.com";
        }
      ];
    }
    """

    result = Parser().parse(text_with_email)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="Foo",
                elements=[
                    ast.Field(
                        name="bar",
                        number=4,
                        type="string",
                        options=[
                            ast.Option(
                                name="(oompa.loompa)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="example",
                                            value="mini@mouse.com",
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_complex_compact_option_with_escaped_string():
    text_with_email = """
    syntax = "proto3";

    message Foo {
      string bar = 4 [
        (oompa.loompa) = {
          example: "\\"blah\\"";
        }
      ];
    }
    """

    print(text_with_email)

    result = Parser().parse(text_with_email)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="Foo",
                elements=[
                    ast.Field(
                        name="bar",
                        number=4,
                        type="string",
                        options=[
                            ast.Option(
                                name="(oompa.loompa)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="example",
                                            value='\\"blah\\"',
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parse_email_compact_option_with_escaped_string():
    text_with_email = """
    syntax = "proto3";

    message Foo {
      string bar = 4 [
        (oompa.loompa) = {
          example: "\\"mini@mouse.com\\"";
        }
      ];
    }
    """

    print(text_with_email)

    result = Parser().parse(text_with_email)
    expected = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Message(
                name="Foo",
                elements=[
                    ast.Field(
                        name="bar",
                        number=4,
                        type="string",
                        options=[
                            ast.Option(
                                name="(oompa.loompa)",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="example",
                                            value='\\"mini@mouse.com\\"',
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
    assert result == expected
