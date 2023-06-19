# pyright: reportOptionalMemberAccess=false

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker

from proto_schema_parser.antlr.ProtobufLexer import ProtobufLexer
from proto_schema_parser.antlr.ProtobufParser import ProtobufParser
from proto_schema_parser.antlr.ProtobufParserListener import ProtobufParserListener
from proto_schema_parser.model import Field, FieldCardinality, Message, Option


class ProtoSchemaParserListener(ProtobufParserListener):
    def __init__(self):
        self.messages: dict[str, Message] = {}
        self.messageStack: list[Message] = []
        self.currentField: Field | None = None

    # Enter a parse tree produced by ProtobufParser#messageDecl.
    def enterMessageDecl(self, ctx: ProtobufParser.MessageDeclContext):
        messageName = ctx.messageName().getText()
        newMessage = Message(name=messageName)
        self.messages[messageName] = newMessage
        self.messageStack.append(newMessage)

    # Exit a parse tree produced by ProtobufParser#messageDecl.
    def exitMessageDecl(self, ctx: ProtobufParser.MessageDeclContext):
        self.messageStack.pop()

    # Enter a parse tree produced by ProtobufParser#messageFieldDecl.
    def enterMessageFieldDecl(self, ctx: ProtobufParser.MessageFieldDeclContext):
        if ctx.messageFieldDeclTypeName() is not None:
            fieldName = ctx.fieldName().getText()
            fieldType = ctx.messageFieldDeclTypeName().getText()
            self.currentField = Field(name=fieldName, type=fieldType)

    # Enter a parse tree produced by ProtobufParser#fieldDeclWithCardinality.
    def enterFieldDeclWithCardinality(
        self, ctx: ProtobufParser.FieldDeclWithCardinalityContext
    ):
        fieldName = ctx.fieldName().getText()
        fieldType = ctx.fieldDeclTypeName().getText()
        cardinality = ctx.fieldCardinality().getText()
        if cardinality == "optional":
            self.currentField = Field(
                name=fieldName, type=fieldType, cardinality=FieldCardinality.OPTIONAL
            )
        elif cardinality == "repeated":
            self.currentField = Field(
                name=fieldName, type=fieldType, cardinality=FieldCardinality.REPEATED
            )
        else:
            self.currentField = Field(
                name=fieldName, type=fieldType, cardinality=FieldCardinality.REQUIRED
            )

    # Exit a parse tree produced by ProtobufParser#messageFieldDecl.
    def exitMessageFieldDecl(self, ctx: ProtobufParser.MessageFieldDeclContext):
        if self.currentField:
            self.messageStack[-1].fields.append(self.currentField)
            self.currentField = None
        else:
            raise Exception("Unexpectedly got currentField=None")

    # Enter a parse tree produced by ProtobufParser#compactOption.
    def enterCompactOption(self, ctx: ProtobufParser.CompactOptionContext):
        optionName = ctx.optionName().getText()
        optionValue = ctx.optionValue().getText()
        option = Option(name=optionName, value=optionValue)
        self.currentField.options.append(option)


class Parser:
    def parse(self, text: str) -> dict[str, Message]:
        input_stream = InputStream(text)
        lexer = ProtobufLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ProtobufParser(stream)
        tree = parser.file_()  # file_ is the start rule for proto3
        listener = ProtoSchemaParserListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener.messages
