from proto_schema_parser import ast
from proto_schema_parser.parser import Parser


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
                                options=[ast.Option(name="default", value="HOME")],
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
                                value="{gte: -90,  lte: 90}",
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
                        value="true",
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
                    ast.Option(name="(my_service_option)", value="FOO"),
                    ast.Method(
                        name="MyMethod",
                        input_type=ast.MessageType(type="RequestType"),
                        output_type=ast.MessageType(type="ResponseType"),
                        elements=[
                            ast.Option(name="(my_method_option).foo", value="567"),
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
                            ast.Option(name="(my_method_option).foo", value="567"),
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
                    ast.Comment(text="// comment on same line"),
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
                            ast.Comment(text="// comment on same line"),
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
                    ast.Comment(text="// comment on same line"),
                    ast.Comment(text="// trailing comment"),
                    ast.Method(
                        name="StreamingFromClient",
                        input_type=ast.MessageType(type="ExampleRequest", stream=True),
                        output_type=ast.MessageType(type="ExampleResponse"),
                        elements=[
                            ast.Comment(text="// comment in RPC"),
                            ast.Option(name="(my_method_option).foo", value="567"),
                            ast.Comment(text="// comment in RPC on same line"),
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
