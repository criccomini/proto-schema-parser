from proto_schema_parser import FieldCardinality, Message, Parser


def test_parser():
    protobuf_text = """
    message Person {
      required string name = 1;
      required int32 id = 2;
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

    result = Parser().parse(protobuf_text)

    assert isinstance(result, dict)
    assert len(result) == 2
    assert "Person" in result
    assert "PhoneNumber" in result

    person = result["Person"]
    assert isinstance(person, Message)
    assert person.name == "Person"

    # Check fields
    assert len(person.fields) == 4

    name_field, id_field, email_field, phones_field = person.fields

    assert name_field.name == "name"
    assert name_field.type == "string"
    assert name_field.cardinality == FieldCardinality.REQUIRED

    assert id_field.name == "id"
    assert id_field.type == "int32"
    assert id_field.cardinality == FieldCardinality.REQUIRED

    assert email_field.name == "email"
    assert email_field.type == "string"
    assert email_field.cardinality == FieldCardinality.OPTIONAL

    assert phones_field.name == "phones"
    assert phones_field.type == "PhoneNumber"
    assert phones_field.cardinality == FieldCardinality.REPEATED

    # Check PhoneNumber
    phone_number = result["PhoneNumber"]
    assert isinstance(phone_number, Message)
    assert phone_number.name == "PhoneNumber"

    # Check PhoneNumber fields
    assert len(phone_number.fields) == 2

    number_field, type_field = phone_number.fields

    assert number_field.name == "number"
    assert number_field.type == "string"
    assert number_field.cardinality == FieldCardinality.OPTIONAL

    assert type_field.name == "type"
    assert type_field.type == "PhoneType"
    assert type_field.cardinality == FieldCardinality.OPTIONAL


def test_parser_search_request():
    protobuf_text = """
    syntax = "proto3";

    message SearchRequest {
      string query = 1 [(validate.rules).double = {gte: -90,  lte: 90}];
      optional int32 page_number = 2;
      option foo = "bar";
      int32 results_per_page = 3;
    }
    """

    result = Parser().parse(protobuf_text)

    assert isinstance(result, dict)
    assert len(result) == 1
    assert "SearchRequest" in result

    search_request = result["SearchRequest"]
    assert isinstance(search_request, Message)
    assert search_request.name == "SearchRequest"

    # Check fields
    assert len(search_request.fields) == 3

    query_field, page_number_field, results_per_page_field = search_request.fields

    assert query_field.name == "query"
    assert query_field.type == "string"
    assert query_field.cardinality == FieldCardinality.REQUIRED
    assert len(query_field.options) == 1
    assert query_field.options[0].name == "(validate.rules).double"
    # Parser trims messageLiteralWithBraces
    assert query_field.options[0].value == "{gte:-90,lte:90}"

    assert page_number_field.name == "page_number"
    assert page_number_field.type == "int32"
    assert page_number_field.cardinality == FieldCardinality.OPTIONAL

    assert results_per_page_field.name == "results_per_page"
    assert results_per_page_field.type == "int32"
    assert results_per_page_field.cardinality == FieldCardinality.REQUIRED


def test_parser_foo_bar_baz():
    protobuf_text = """
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

    result = Parser().parse(protobuf_text)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert "Foo" in result
    assert "Bar" in result
    assert "Baz" in result

    foo = result["Foo"]
    bar = result["Bar"]
    baz = result["Baz"]

    assert isinstance(foo, Message)
    assert foo.name == "Foo"
    assert len(foo.fields) == 1
    assert foo.fields[0].name == "baz"
    assert foo.fields[0].type == "Baz"
    assert foo.fields[0].cardinality == FieldCardinality.OPTIONAL

    assert isinstance(bar, Message)
    assert bar.name == "Bar"
    assert len(bar.fields) == 2
    assert bar.fields[0].name == "name"
    assert bar.fields[0].type == "string"
    assert bar.fields[0].cardinality == FieldCardinality.REQUIRED
    assert bar.fields[1].name == "value"
    assert bar.fields[1].type == "string"
    assert bar.fields[1].cardinality == FieldCardinality.REQUIRED

    assert isinstance(baz, Message)
    assert baz.name == "Baz"
    assert len(baz.fields) == 1
    assert baz.fields[0].name == "a"
    assert baz.fields[0].type == "Bar"
    assert baz.fields[0].cardinality == FieldCardinality.REQUIRED
