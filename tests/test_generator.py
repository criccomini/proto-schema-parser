from proto_schema_parser import ast
from proto_schema_parser.generator import Generator


def test_generate_simple_message():
    message = ast.Message(
        name="MyMessage",
        elements=[
            ast.Field(
                name="my_field",
                type="string",
                number=1,
                cardinality=ast.FieldCardinality.OPTIONAL,
            ),
            ast.Field(
                name="another_field",
                type="int32",
                number=2,
                cardinality=ast.FieldCardinality.REQUIRED,
            ),
        ],
    )

    result = Generator()._generate_message(message)
    expected = (
        "message MyMessage {\n"
        "  optional string my_field = 1;\n"
        "  required int32 another_field = 2;\n"
        "}"
    )

    assert result == expected


def test_generate_package():
    file = ast.File(file_elements=[ast.Package(name="my.package")])

    result = Generator().generate(file)
    expected = "package my.package;"

    assert result == expected


def test_generate_import():
    file = ast.File(file_elements=[ast.Import(name="my/import/path.proto")])

    result = Generator().generate(file)
    expected = 'import "my/import/path.proto";'

    assert result == expected


def test_generate_option():
    file = ast.File(
        file_elements=[ast.Option(name="java_package", value="com.example.myproto")]
    )

    result = Generator().generate(file)
    expected = 'option java_package = "com.example.myproto";'

    assert result == expected


def test_generate_enum():
    file = ast.File(
        file_elements=[
            ast.Enum(
                name="MyEnum",
                elements=[
                    ast.EnumValue(name="FIRST_VALUE", number=0),
                    ast.EnumValue(name="SECOND_VALUE", number=1),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = "enum MyEnum {\n" "  FIRST_VALUE = 0;\n" "  SECOND_VALUE = 1;\n" "}"

    assert result == expected


def test_generate_extension():
    file = ast.File(
        file_elements=[
            ast.Extension(
                typeName="ExtendeeType",
                elements=[
                    ast.Field(
                        name="ext_field",
                        type="string",
                        number=1,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                    ),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = "extend ExtendeeType {\n" "  optional string ext_field = 1;\n" "}"

    assert result == expected


def test_generate_extension_with_comment():
    file = ast.File(
        file_elements=[
            ast.Extension(
                typeName="ExtendeeType",
                elements=[
                    ast.Comment(text="// This is a comment. "),
                    ast.Field(
                        name="ext_field",
                        type="string",
                        number=1,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                    ),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = (
        "extend ExtendeeType {\n"
        "  // This is a comment. \n  optional string ext_field = 1;\n"
        "}"
    )

    assert result == expected


def test_generate_nested_message():
    file = ast.File(
        file_elements=[
            ast.Message(
                name="OuterMessage",
                elements=[
                    ast.Message(
                        name="InnerMessage",
                        elements=[
                            ast.Field(
                                name="inner_field",
                                type="int32",
                                number=1,
                                cardinality=ast.FieldCardinality.REQUIRED,
                            ),
                        ],
                    ),
                    ast.Field(
                        name="outer_field",
                        type="InnerMessage",
                        number=2,
                    ),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = (
        "message OuterMessage {\n"
        "  message InnerMessage {\n"
        "    required int32 inner_field = 1;\n"
        "  }\n"
        "  InnerMessage outer_field = 2;\n"
        "}"
    )

    assert result == expected


def test_generate_map_field():
    map_field = ast.MapField(
        name="my_map",
        key_type="string",
        value_type="int32",
        number=2,
    )

    result = Generator()._generate_map_field(map_field)
    expected = "map<string, int32> my_map = 2;"

    assert result == expected


def test_generate_group():
    group = ast.Group(
        name="MyGroup",
        number=1,
        elements=[
            ast.Field(
                name="my_field",
                type="string",
                number=2,
                cardinality=ast.FieldCardinality.OPTIONAL,
            ),
        ],
    )

    result = Generator()._generate_group(group)
    expected = "group MyGroup = 1 {\n" "  optional string my_field = 2;\n" "}"

    assert result == expected


def test_generate_one_of():
    file = ast.File(
        file_elements=[
            ast.Message(
                name="MyMessage",
                elements=[
                    ast.OneOf(
                        name="my_one_of",
                        elements=[
                            ast.Field(
                                name="my_field",
                                type="string",
                                number=1,
                                cardinality=ast.FieldCardinality.OPTIONAL,
                            ),
                            ast.Field(
                                name="my_field_2",
                                type="int32",
                                number=2,
                                cardinality=ast.FieldCardinality.OPTIONAL,
                            ),
                        ],
                    ),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = (
        "message MyMessage {\n"
        "  oneof my_one_of {\n"
        "    optional string my_field = 1;\n"
        "    optional int32 my_field_2 = 2;\n"
        "  }\n"
        "}"
    )

    assert result == expected


def test_generate_extension_range():
    file = ast.File(
        file_elements=[
            ast.Message(
                name="MyMessage",
                elements=[
                    ast.ExtensionRange(
                        ranges=["100 to 199", "300 to max"],
                    ),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = "message MyMessage {\n" "  extensions 100 to 199, 300 to max;\n" "}"

    assert result == expected


def test_generate_reserved():
    file = ast.File(
        file_elements=[
            ast.Message(
                name="MyMessage",
                elements=[
                    ast.Reserved(
                        ranges=["1 to 8", "10", "12"],
                        names=['"foo"', '"bar"'],
                    ),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = "message MyMessage {\n" '  reserved 1 to 8, 10, 12, "foo", "bar";\n' "}"

    assert result == expected


def test_generate_with_options():
    file = ast.File(
        file_elements=[
            ast.Option(name="java_package", value="com.example.myproto"),
            ast.Message(
                name="MyMessage",
                elements=[
                    ast.Option(name="deprecated", value="true"),
                    ast.Field(
                        name="my_field",
                        type="string",
                        number=1,
                        options=[ast.Option(name="default", value="default_value")],
                    ),
                    ast.OneOf(
                        name="my_oneof",
                        elements=[
                            ast.Option(name="deprecated", value="true"),
                            ast.Field(
                                name="oneof_field",
                                type="string",
                                number=2,
                                options=[
                                    ast.Option(name="default", value="oneof_default")
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ast.Enum(
                name="MyEnum",
                elements=[
                    ast.Option(name="allow_alias", value="true"),
                    ast.EnumValue(name="FIRST_VALUE", number=0),
                ],
            ),
        ]
    )

    result = Generator().generate(file)
    expected = (
        'option java_package = "com.example.myproto";\n'
        "message MyMessage {\n"
        '  option deprecated = "true";\n'
        '  string my_field = 1 [default = "default_value"];\n'
        "  oneof my_oneof {\n"
        '    option deprecated = "true";\n'
        '    string oneof_field = 2 [default = "oneof_default"];\n'
        "  }\n"
        "}\n"
        "enum MyEnum {\n"
        '  option allow_alias = "true";\n'
        "  FIRST_VALUE = 0;\n"
        "}"
    )

    assert result == expected


def test_generate_service():
    file = ast.File(
        file_elements=[
            ast.Service(
                name="MyService",
                elements=[
                    ast.Method(
                        name="MyRpc",
                        input_type=ast.MessageType(type="MyRequest"),
                        output_type=ast.MessageType(type="MyResponse"),
                    ),
                    ast.Method(
                        name="MyRpcWithStream",
                        input_type=ast.MessageType(type="MyRequest", stream=True),
                        output_type=ast.MessageType(type="MyResponse"),
                    ),
                    ast.Method(
                        name="MyRpcWithOption",
                        input_type=ast.MessageType(type="MyRequest"),
                        output_type=ast.MessageType(type="MyResponse"),
                        elements=[ast.Option(name="deprecated", value="true")],
                    ),
                    ast.Option(name="MyOption", value="foo"),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = (
        "service MyService {\n"
        "  rpc MyRpc (MyRequest) returns (MyResponse);\n"
        "  rpc MyRpcWithStream (stream MyRequest) returns (MyResponse);\n"
        "  rpc MyRpcWithOption (MyRequest) returns (MyResponse){\n"
        '    option deprecated = "true";\n'
        "  }\n"
        '  option MyOption = "foo";\n'
        "}"
    )

    assert result == expected


def test_message_with_comments():
    file = ast.File(
        file_elements=[
            ast.Comment(text="// This is a comment"),
            ast.Message(
                name="MyMessage",
                elements=[
                    ast.Comment(text="/* This is a block comment */"),
                    ast.Field(
                        name="my_field",
                        type="string",
                        number=1,
                        cardinality=ast.FieldCardinality.OPTIONAL,
                    ),
                    ast.Comment(text="/* This is a multi-line\n  block comment */"),
                    ast.Field(
                        name="another_field",
                        type="int32",
                        number=2,
                        cardinality=ast.FieldCardinality.REQUIRED,
                    ),
                ],
            ),
        ]
    )

    result = Generator().generate(file)
    expected = (
        "// This is a comment\n"
        "message MyMessage {\n"
        "  /* This is a block comment */\n"
        "  optional string my_field = 1;\n"
        "  /* This is a multi-line\n"
        "  block comment */\n"
        "  required int32 another_field = 2;\n"
        "}"
    )

    assert result == expected


def test_enum_with_comments():
    file = ast.File(
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
                    ast.Comment(text="/* Multi-line\n    comment */"),
                ],
            ),
        ],
    )
    result = Generator().generate(file)
    expected = (
        "enum SampleEnum {\n"
        "  // This is a comment\n"
        "  UNKNOWN = 0;\n"
        "  SOMETHING = 1;\n"
        "  // comment on same line\n"
        "  ELSE = 2;\n"
        "  // trailing comment\n"
        "  MORE = 3;\n"
        "  /* Multi-line\n"
        "    comment */\n"
        "}"
    )

    assert result == expected


def test_oneof_with_comments():
    file = ast.File(
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
                            ast.Comment(text="/* multi-line\n    comment*/"),
                        ],
                    ),
                ],
            ),
        ],
    )
    result = Generator().generate(file)

    expected = (
        "message TestMessage {\n"
        "  oneof test_oneof {\n"
        "    // This is a comment\n"
        "    string name = 1;\n"
        "    int32 id = 2;\n"
        "    // comment on same line\n"
        "    // trailing comment\n"
        "    bool active = 3;\n"
        "    /* multi-line\n"
        "    comment*/\n"
        "  }\n"
        "}"
    )

    assert result == expected
