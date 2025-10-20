from proto_schema_parser import ast
from proto_schema_parser.generator import Generator
from proto_schema_parser.parser import Parser


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
                        names=["foo", "bar"],
                    ),
                    ast.Reserved(
                        ranges=["13 to 17", "27", "54"],
                        names=[],
                    ),
                    ast.Reserved(
                        ranges=[],
                        names=["spam", "spamspam"],
                    ),
                ],
            )
        ]
    )

    result = Generator().generate(file)
    expected = (
        "message MyMessage {\n"
        '  reserved 1 to 8, 10, 12, "foo", "bar";\n  reserved 13 to 17, 27, 54;\n  reserved "spam", "spamspam";\n'
        "}"
    )

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
        "  rpc MyRpcWithOption (MyRequest) returns (MyResponse) {\n"
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


def test_generate_service_with_numeric_option():
    file = ast.File(
        syntax="proto3",
        file_elements=[
            ast.Package(name="test.v1.proto_1"),
            ast.Service(
                name="TestService",
                elements=[
                    ast.Option(
                        name="test.options.v1.lifecycle",
                        value=ast.Identifier("DEPRECATED"),
                    ),
                    ast.Option(name="test.options.v1.major_version", value=1),
                ],
            ),
        ],
    )
    result = Generator().generate(file)

    expected = (
        'syntax = "proto3";\n'
        "package test.v1.proto_1;\n"
        "service TestService {\n"
        "  option test.options.v1.lifecycle = DEPRECATED;\n"
        "  option test.options.v1.major_version = 1;\n"
        "}"
    )

    assert result == expected


def test_generate_field_option_with_message_literal():
    schema = """message FieldAttr {
  string text = 1;
}

message FieldAttributes {
  optional FieldAttr attr = 1;
}

extend google.protobuf.FieldOptions {
  optional FieldAttributes field_attributes = 50001;
}

message MyMessage {
  string title = 1 [
    (field_attributes).attr = { text: "a" },
  ];
}
"""

    file = Parser().parse(schema)

    result = Generator().generate(file)
    expected = (
        "message FieldAttr {\n"
        "  string text = 1;\n"
        "}\n"
        "message FieldAttributes {\n"
        "  optional FieldAttr attr = 1;\n"
        "}\n"
        "extend google.protobuf.FieldOptions {\n"
        "  optional FieldAttributes field_attributes = 50001;\n"
        "}\n"
        "message MyMessage {\n"
        '  string title = 1 [(field_attributes).attr = { text: "a" }];\n'
        "}"
    )

    assert result == expected


def test_generate_field_option_with_nested_empty_message_literal():
    schema = """message FieldAttr {
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

    file = Parser().parse(schema)

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

    result = Generator().generate(file)
    expected = (
        "message FieldAttr {\n"
        "  message Nested {\n"
        "    string text = 1;\n"
        "  }\n"
        "  Nested nested = 1;\n"
        "}\n"
        "message FieldAttributes {\n"
        "  optional FieldAttr attr = 1;\n"
        "}\n"
        "extend google.protobuf.FieldOptions {\n"
        "  optional FieldAttributes field_attributes = 50001;\n"
        "}\n"
        "message MyMessage {\n"
        "  string title = 1 [(field_attributes).attr = { nested: {} }];\n"
        "}"
    )

    assert result == expected

    round_trip = Parser().parse(result)
    assert round_trip == file


def test_generate_message_literal_with_braces():
    file = ast.File(
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
    result = Generator().generate(file)
    expected = (
        'syntax = "proto3";\n'
        "message SearchRequest {\n"
        "  option (custom_option) = {\n"
        '    field1: "value1",\n'
        "    field2: 42,\n"
        "    nested_field: {\n"
        '      key1: "nested_value1",\n'
        "      key2: [1, 2, 3]\n"
        "    }\n"
        "  };\n"
        "  string query = 1;\n"
        "}"
    )
    assert result == expected


def test_generate_option_with_simple_message_literal():
    option = ast.Option(
        name="my_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(name="field1", value="value1"),
                ast.MessageLiteralField(name="field2", value=42),
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = "option my_option = {\n" '  field1: "value1",\n' "  field2: 42\n" "};"

    assert result == expected


def test_generate_option_with_nested_message_literal():
    option = ast.Option(
        name="nested_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(
                    name="outer_field",
                    value=ast.MessageLiteral(
                        elements=[
                            ast.MessageLiteralField(name="inner_field", value=True)
                        ]
                    ),
                )
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = (
        "option nested_option = {\n"
        "  outer_field: {\n"
        "    inner_field: true\n"
        "  }\n"
        "};"
    )

    assert result == expected


def test_generate_option_with_list_literal():
    option = ast.Option(
        name="list_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(
                    name="field",
                    value=[
                        1,
                        2,
                        3,
                    ],
                )
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = "option list_option = {\n" "  field: [1, 2, 3]\n" "};"

    assert result == expected


def test_generate_option_with_empty_message_literal():
    option = ast.Option(
        name="empty_option",
        value=ast.MessageLiteral(elements=[]),
    )

    result = Generator()._generate_option(option)
    expected = "option empty_option = {};"

    assert result == expected


def test_generate_option_with_identifier():
    option = ast.Option(
        name="identifier_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(
                    name="id", value=ast.Identifier(name="MyIdentifier")
                )
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = "option identifier_option = {\n" "  id: MyIdentifier\n" "};"

    assert result == expected


def test_generate_option_with_complex_message_literal():
    option = ast.Option(
        name="complex_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(
                    name="nested_field",
                    value=ast.MessageLiteral(
                        elements=[
                            ast.MessageLiteralField(name="inner1", value="string"),
                            ast.MessageLiteralField(name="inner2", value=False),
                        ]
                    ),
                ),
                ast.MessageLiteralField(name="scalar_field", value=123.45),
                ast.MessageLiteralField(
                    name="list_field",
                    value=[
                        "item1",
                        "item2",
                    ],
                ),
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = (
        "option complex_option = {\n"
        "  nested_field: {\n"
        '    inner1: "string",\n'
        "    inner2: false\n"
        "  },\n"
        "  scalar_field: 123.45,\n"
        '  list_field: ["item1", "item2"]\n'
        "};"
    )

    assert result == expected


def test_generate_option_with_inconsistent_indentation():
    option = ast.Option(
        name="indented_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(
                    name="level1",
                    value=ast.MessageLiteral(
                        elements=[
                            ast.MessageLiteralField(
                                name="level2",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="field", value="deep_value"
                                        )
                                    ]
                                ),
                            )
                        ]
                    ),
                )
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = (
        "option indented_option = {\n"
        "  level1: {\n"
        "    level2: {\n"
        '      field: "deep_value"\n'
        "    }\n"
        "  }\n"
        "};"
    )

    assert result == expected


def test_generate_option_with_message_literal_in_message():
    file = ast.File(
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

    result = Generator().generate(file)
    expected = (
        'syntax = "proto3";\n'
        "message SearchRequest {\n"
        "  option (custom_option) = {\n"
        '    field1: "value1",\n'
        "    field2: 42,\n"
        "    nested_field: {\n"
        '      key1: "nested_value1",\n'
        "      key2: [1, 2, 3]\n"
        "    }\n"
        "  };\n"
        "  string query = 1;\n"
        "}"
    )

    assert result == expected


def test_generate_service_with_option_message_literal():
    file = ast.File(
        file_elements=[
            ast.Service(
                name="TestService",
                elements=[
                    ast.Option(
                        name="service_option",
                        value=ast.MessageLiteral(
                            elements=[
                                ast.MessageLiteralField(name="bool_field", value=True),
                                ast.MessageLiteralField(name="number_field", value=123),
                                ast.MessageLiteralField(
                                    name="string_field", value="test"
                                ),
                                ast.MessageLiteralField(
                                    name="list_field",
                                    value=["a", "b"],
                                ),
                            ]
                        ),
                    ),
                    ast.Method(
                        name="TestMethod",
                        input_type=ast.MessageType(type="TestRequest"),
                        output_type=ast.MessageType(type="TestResponse"),
                        elements=[
                            ast.Option(
                                name="method_option",
                                value=ast.MessageLiteral(
                                    elements=[
                                        ast.MessageLiteralField(
                                            name="inner_option",
                                            value=ast.MessageLiteral(
                                                elements=[
                                                    ast.MessageLiteralField(
                                                        name="enabled", value=False
                                                    )
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                ],
            )
        ],
    )

    result = Generator().generate(file)
    expected = (
        "service TestService {\n"
        "  option service_option = {\n"
        "    bool_field: true,\n"
        "    number_field: 123,\n"
        '    string_field: "test",\n'
        '    list_field: ["a", "b"]\n'
        "  };\n"
        "  rpc TestMethod (TestRequest) returns (TestResponse) {\n"
        "    option method_option = {\n"
        "      inner_option: {\n"
        "        enabled: false\n"
        "      }\n"
        "    };\n"
        "  }\n"
        "}"
    )

    assert result == expected


def test_generate_option_with_list_of_messages():
    option = ast.Option(
        name="list_of_messages_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(
                    name="messages",
                    value=[
                        ast.MessageLiteral(
                            elements=[
                                ast.MessageLiteralField(name="id", value=1),
                                ast.MessageLiteralField(name="name", value="First"),
                            ]
                        ),
                        ast.MessageLiteral(
                            elements=[
                                ast.MessageLiteralField(name="id", value=2),
                                ast.MessageLiteralField(name="name", value="Second"),
                            ]
                        ),
                    ],
                )
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = (
        "option list_of_messages_option = {\n"
        "  messages: [{\n"
        "    id: 1,\n"
        '    name: "First"\n'
        "  }, {\n"
        "    id: 2,\n"
        '    name: "Second"\n'
        "  }]\n"
        "};"
    )
    assert result == expected


def test_generate_option_with_empty_list():
    option = ast.Option(
        name="empty_list_option",
        value=ast.MessageLiteral(
            elements=[ast.MessageLiteralField(name="items", value=[])]
        ),
    )

    result = Generator()._generate_option(option)
    expected = "option empty_list_option = {\n" "  items: []\n" "};"

    assert result == expected


def test_trailing_comments_exhaustive_complex_schema_generator():
    """
    Validate generator preserves trailing comments across a complex schema.

    Uses the same TC markers as the parser test. We expect failures until
    all contexts (e.g., message literals) preserve comments in the AST.
    """

    schema = """syntax = "proto3"; // TC#1 syntax
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
    c: { // TC#12a inner inline message
      x: "y" // TC#12b inner inline message
    } // TC#12c inner inline message
  }, // TC#13 inner end with comma
  list_of_msgs: [{ // TC#14a list of messages
    i: 1 // TC#14b list of messages
  }, { // TC#14c list of messages
    i: 2 // TC#14d list of messages
  }] // TC#14e list of messages
}; // TC#15 option msg end
message Outer { // TC#16 message open
  option deprecated = true; // TC#17 message option
  required string name = 1; // TC#18 field required
  optional int32 id = 2 [packed = true]; // TC#19 field with compact options
  map<string, int64> attrs = 3; // TC#20 map field
  group InnerGroup = 4 { // TC#21 group open
    optional bool flag = 1; // TC#22 group field
  } // TC#23 group close
  oneof choice { // TC#24 oneof open
    string a = 5; // TC#25 oneof field a
    group G = 6 { // TC#26 oneof group open
      int32 v = 1; // TC#27 oneof group field
    } // TC#28 oneof group close
  } // TC#29 oneof close
  extensions 100 to 199, 500 to max; // TC#30 extensions
  reserved 8, 9 to 11; // TC#31 reserved ranges
  reserved "foo", "bar"; // TC#31b reserved names
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
  group ExtG = 1001 { // TC#43 extension group open
    int32 ev = 1; // TC#44 extension group field
  } // TC#45 extension group close
} // TC#46 extension decl close
service Svc { // TC#47 service open
  option (company.svc_opt) = { // TC#48 service option open
    get: "/v1/x", // TC#49 service opt field get
    additional_bindings: { // TC#50 nested msg literal open
      post: "/v1/y" // TC#51 nested field post
    } // TC#52 nested msg literal close
  }; // TC#53 service option close
  rpc Unary (Outer) returns (Nested); // TC#54 rpc simple
  rpc Bidi (stream Outer) returns (stream Outer) { // TC#55 rpc block open
    option (company.mtd_opt).num = 7; // TC#56 method option
  } // TC#57 rpc block close
} // TC#58 service close
/*
not inline
*/"""

    file = Parser().parse(schema)
    generated = Generator().generate(file)

    assert generated == schema


def test_generate_option_with_special_float_values():
    option = ast.Option(
        name="float_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(name="infinite", value=ast.Identifier("inf")),
                ast.MessageLiteralField(
                    name="negative_infinite", value=ast.Identifier("-inf")
                ),
                ast.MessageLiteralField(name="nan_value", value=ast.Identifier("nan")),
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = (
        "option float_option = {\n"
        "  infinite: inf,\n"
        "  negative_infinite: -inf,\n"
        "  nan_value: nan\n"
        "};"
    )

    assert result == expected


def test_generate_option_with_boolean_values():
    option = ast.Option(
        name="bool_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(name="flag_true", value=True),
                ast.MessageLiteralField(name="flag_false", value=False),
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = (
        "option bool_option = {\n" "  flag_true: true,\n" "  flag_false: false\n" "};"
    )

    assert result == expected


def test_generate_option_with_special_characters_in_string():
    option = ast.Option(
        name="string_option",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(
                    name="special_string", value='This is a "quote" and a \\ backslash'
                )
            ]
        ),
    )

    result = Generator()._generate_option(option)
    expected = (
        "option string_option = {\n"
        '  special_string: "This is a \\"quote\\" and a \\\\ backslash"\n'
        "};"
    )

    assert result == expected


def test_generate_option_with_multiple_message_literals():
    option1 = ast.Option(
        name="option_one",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(name="field1", value="value1"),
            ]
        ),
    )

    option2 = ast.Option(
        name="option_two",
        value=ast.MessageLiteral(
            elements=[
                ast.MessageLiteralField(name="field2", value="value2"),
            ]
        ),
    )

    message = ast.Message(
        name="MyMessage",
        elements=[
            option1,
            option2,
            ast.Field(
                name="my_field",
                type="string",
                number=1,
                cardinality=ast.FieldCardinality.OPTIONAL,
            ),
        ],
    )

    result = Generator()._generate_message(message)
    expected = (
        "message MyMessage {\n"
        "  option option_one = {\n"
        '    field1: "value1"\n'
        "  };\n"
        "  option option_two = {\n"
        '    field2: "value2"\n'
        "  };\n"
        "  optional string my_field = 1;\n"
        "}"
    )

    assert result == expected


def test_generate_field_with_options_for_scalar_types():
    generator = Generator()
    test_cases = [
        # Numeric types
        ("double", 3.14, "double field_double = 1 [default = 3.14];"),
        ("float", -1.23, "float field_float = 2 [default = -1.23];"),
        ("int32", -42, "int32 field_int32 = 3 [default = -42];"),
        ("int64", 9876543210, "int64 field_int64 = 4 [default = 9876543210];"),
        ("uint32", 42, "uint32 field_uint32 = 5 [default = 42];"),
        ("uint64", 1234567890, "uint64 field_uint64 = 6 [default = 1234567890];"),
        ("sint32", -123, "sint32 field_sint32 = 7 [default = -123];"),
        ("sint64", -9876543210, "sint64 field_sint64 = 8 [default = -9876543210];"),
        ("fixed32", 456, "fixed32 field_fixed32 = 9 [default = 456];"),
        ("fixed64", 1234567890, "fixed64 field_fixed64 = 10 [default = 1234567890];"),
        ("sfixed32", -789, "sfixed32 field_sfixed32 = 11 [default = -789];"),
        (
            "sfixed64",
            -1234567890,
            "sfixed64 field_sfixed64 = 12 [default = -1234567890];",
        ),
        # Boolean type
        ("bool", True, "bool field_bool = 13 [default = true];"),
        # String types
        (
            "string",
            "test string",
            'string field_string = 14 [default = "test string"];',
        ),
    ]

    for type_name, default_value, expected in test_cases:
        field = ast.Field(
            name=f"field_{type_name}",
            type=type_name,
            number=test_cases.index((type_name, default_value, expected)) + 1,
            options=[ast.Option(name="default", value=default_value)],
        )
        result = generator._generate_field(field)
        assert result == expected


def test_generate_service_with_additional_bindings():
    """Test that a service with additional_bindings in google.api.http option is generated correctly."""
    service = ast.Service(
        name="Lease",
        elements=[
            ast.Method(
                name="LeaseRevoke",
                input_type=ast.MessageType(type="LeaseRevokeRequest", stream=False),
                output_type=ast.MessageType(type="LeaseRevokeResponse", stream=False),
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
                                                name="post", value="/v3/kv/lease/revoke"
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

    result = Generator()._generate_service(service)
    expected = (
        "service Lease {\n"
        "  rpc LeaseRevoke (LeaseRevokeRequest) returns (LeaseRevokeResponse) {\n"
        "    option (google.api.http) = {\n"
        '      post: "/v3/lease/revoke",\n'
        '      body: "*",\n'
        "      additional_bindings: {\n"
        '        post: "/v3/kv/lease/revoke",\n'
        '        body: "*"\n'
        "      }\n"
        "    };\n"
        "  }\n"
        "}"
    )

    assert result == expected


def test_generate_option_with_complex_nested_message_literal_swagger():
    """Test that a complex message literal with nested security definitions is generated correctly."""
    file = ast.File(
        file_elements=[
            ast.Option(
                name="(grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger)",
                value=ast.MessageLiteral(
                    elements=[
                        ast.MessageLiteralField(
                            name="security_definitions",
                            value=ast.MessageLiteral(
                                elements=[
                                    ast.MessageLiteralField(
                                        name="security",
                                        value=ast.MessageLiteral(
                                            elements=[
                                                ast.MessageLiteralField(
                                                    name="key", value="ApiKey"
                                                ),
                                                ast.MessageLiteralField(
                                                    name="value",
                                                    value=ast.MessageLiteral(
                                                        elements=[
                                                            ast.MessageLiteralField(
                                                                name="type",
                                                                value=ast.Identifier(
                                                                    name="TYPE_API_KEY"
                                                                ),
                                                            ),
                                                            ast.MessageLiteralField(
                                                                name="in",
                                                                value=ast.Identifier(
                                                                    name="IN_HEADER"
                                                                ),
                                                            ),
                                                            ast.MessageLiteralField(
                                                                name="name",
                                                                value="Authorization",
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                        ),
                        ast.MessageLiteralField(
                            name="security",
                            value=ast.MessageLiteral(
                                elements=[
                                    ast.MessageLiteralField(
                                        name="security_requirement",
                                        value=ast.MessageLiteral(
                                            elements=[
                                                ast.MessageLiteralField(
                                                    name="key", value="ApiKey"
                                                ),
                                                ast.MessageLiteralField(
                                                    name="value",
                                                    value=ast.MessageLiteral(
                                                        elements=[]
                                                    ),
                                                ),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                        ),
                    ]
                ),
            )
        ]
    )

    result = Generator().generate(file)
    expected = """option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger) = {
  security_definitions: {
    security: {
      key: "ApiKey",
      value: {
        type: TYPE_API_KEY,
        in: IN_HEADER,
        name: "Authorization"
      }
    }
  },
  security: {
    security_requirement: {
      key: "ApiKey",
      value: {}
    }
  }
};"""

    assert result == expected


def test_generate_multiple_options_with_complex_message_literals():
    """Test that multiple options with complex message literals are generated correctly."""
    file = ast.File(
        file_elements=[
            ast.Option(name="go_package", value="go.etcd.io/etcd/api/v3/etcdserverpb"),
            ast.Option(name="(gogoproto.marshaler_all)", value=True),
            ast.Option(name="(gogoproto.unmarshaler_all)", value=True),
            ast.Option(
                name="(grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger)",
                value=ast.MessageLiteral(
                    elements=[
                        ast.MessageLiteralField(
                            name="security_definitions",
                            value=ast.MessageLiteral(
                                elements=[
                                    ast.MessageLiteralField(
                                        name="security",
                                        value=ast.MessageLiteral(
                                            elements=[
                                                ast.MessageLiteralField(
                                                    name="key", value="ApiKey"
                                                ),
                                                ast.MessageLiteralField(
                                                    name="value",
                                                    value=ast.MessageLiteral(
                                                        elements=[
                                                            ast.MessageLiteralField(
                                                                name="type",
                                                                value=ast.Identifier(
                                                                    name="TYPE_API_KEY"
                                                                ),
                                                            ),
                                                            ast.MessageLiteralField(
                                                                name="in",
                                                                value=ast.Identifier(
                                                                    name="IN_HEADER"
                                                                ),
                                                            ),
                                                            ast.MessageLiteralField(
                                                                name="name",
                                                                value="Authorization",
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                        ),
                        ast.MessageLiteralField(
                            name="security",
                            value=ast.MessageLiteral(
                                elements=[
                                    ast.MessageLiteralField(
                                        name="security_requirement",
                                        value=ast.MessageLiteral(
                                            elements=[
                                                ast.MessageLiteralField(
                                                    name="key", value="ApiKey"
                                                ),
                                                ast.MessageLiteralField(
                                                    name="value",
                                                    value=ast.MessageLiteral(
                                                        elements=[]
                                                    ),
                                                ),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ]
    )

    result = Generator().generate(file)
    expected = """option go_package = "go.etcd.io/etcd/api/v3/etcdserverpb";
option (gogoproto.marshaler_all) = true;
option (gogoproto.unmarshaler_all) = true;
option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_swagger) = {
  security_definitions: {
    security: {
      key: "ApiKey",
      value: {
        type: TYPE_API_KEY,
        in: IN_HEADER,
        name: "Authorization"
      }
    }
  },
  security: {
    security_requirement: {
      key: "ApiKey",
      value: {}
    }
  }
};"""

    assert result == expected


def test_option_with_comments_in_message_literal():
    expected = """syntax = "proto3";
message Example {
  option (policy) = {
    foo: "bar" // comment should be preserved
  };
}"""

    file = Parser().parse(expected)
    result = Generator().generate(file)
    assert result == expected
