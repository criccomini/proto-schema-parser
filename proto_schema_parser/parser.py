# pyright: reportOptionalMemberAccess=false, reportOptionalIterable=false

from typing import Any

from antlr4 import CommonTokenStream, InputStream

from proto_schema_parser import ast
from proto_schema_parser.antlr.ProtobufLexer import ProtobufLexer
from proto_schema_parser.antlr.ProtobufParser import ProtobufParser
from proto_schema_parser.antlr.ProtobufParserVisitor import ProtobufParserVisitor


class ASTConstructor(ProtobufParserVisitor):
    def visitFile(self, ctx: ProtobufParser.FileContext):
        syntax = (
            self._getText(ctx.syntaxDecl().syntaxLevel()) if ctx.syntaxDecl() else None
        )
        file_elements = [self.visit(child) for child in ctx.commentDecl()] + [
            self.visit(child) for child in ctx.fileElement()
        ]
        return ast.File(syntax=syntax, file_elements=file_elements)

    def visitCommentDecl(self, ctx: ProtobufParser.CommentDeclContext):
        return ast.Comment(text=self._getText(ctx))

    def visitPackageDecl(self, ctx: ProtobufParser.PackageDeclContext):
        name = self._getText(ctx.packageName())
        return ast.Package(name=name)

    def visitImportDecl(self, ctx: ProtobufParser.ImportDeclContext):
        name = self._getText(ctx.importedFileName())
        weak = ctx.WEAK() is not None
        public = ctx.PUBLIC() is not None
        return ast.Import(name=name, weak=weak, public=public)

    def visitOptionDecl(self, ctx: ProtobufParser.OptionDeclContext):
        name = self._getText(ctx.optionName())
        value = self._getText(ctx.optionValue())
        return ast.Option(name=name, value=value)

    def visitMessageDecl(self, ctx: ProtobufParser.MessageDeclContext):
        name = self._getText(ctx.messageName())
        elements = [self.visit(child) for child in ctx.messageElement()]
        return ast.Message(name=name, elements=elements)

    def visitMessageFieldDecl(self, ctx: ProtobufParser.MessageFieldDeclContext):
        if fieldWithCardinality := ctx.fieldDeclWithCardinality():
            return self.visit(fieldWithCardinality)
        else:
            name = self._getText(ctx.fieldName())
            number = int(self._getText(ctx.fieldNumber()))
            type = self._getText(ctx.messageFieldDeclTypeName())
            options = self.visit(ctx.compactOptions()) if ctx.compactOptions() else []
            return ast.Field(
                name=name,
                number=number,
                type=type,
                options=options,
            )

    def visitFieldDeclWithCardinality(
        self, ctx: ProtobufParser.FieldDeclWithCardinalityContext
    ):
        name = self._getText(ctx.fieldName())
        number = int(self._getText(ctx.fieldNumber()))
        cardinality = None
        if ctx.fieldCardinality().OPTIONAL():
            cardinality = ast.FieldCardinality.OPTIONAL
        elif ctx.fieldCardinality().REQUIRED():
            cardinality = ast.FieldCardinality.REQUIRED
        elif ctx.fieldCardinality().REPEATED():
            cardinality = ast.FieldCardinality.REPEATED
        type = self._getText(ctx.fieldDeclTypeName())
        options = self.visit(ctx.compactOptions()) if ctx.compactOptions() else []
        return ast.Field(
            name=name,
            number=number,
            cardinality=cardinality,
            type=type,
            options=options,
        )

    def visitCompactOption(self, ctx: ProtobufParser.CompactOptionContext):
        name = self._getText(ctx.optionName())
        value = self._getText(ctx.optionValue())
        return ast.Option(name=name, value=value)

    def visitCompactOptions(self, ctx: ProtobufParser.CompactOptionsContext):
        return [self.visit(child) for child in ctx.compactOption()]

    def visitOneofFieldDecl(self, ctx: ProtobufParser.OneofFieldDeclContext):
        name = self._getText(ctx.fieldName())
        number = int(self._getText(ctx.fieldNumber()))
        type = self._getText(ctx.oneofFieldDeclTypeName())
        options = self.visit(ctx.compactOptions()) if ctx.compactOptions() else []
        return ast.Field(
            name=name,
            number=number,
            type=type,
            options=options,
        )

    def visitOneofGroupDecl(self, ctx: ProtobufParser.OneofGroupDeclContext):
        name = self._getText(ctx.fieldName())
        number = int(self._getText(ctx.fieldNumber()))
        elements = [self.visit(child) for child in ctx.messageElement()]
        return ast.Group(
            name=name,
            number=number,
            elements=elements,
        )

    def visitMapFieldDecl(self, ctx: ProtobufParser.MapFieldDeclContext):
        name = self._getText(ctx.fieldName())
        number = int(self._getText(ctx.fieldNumber()))
        key_type = self._getText(ctx.mapType().mapKeyType())
        value_type = self._getText(ctx.mapType().typeName())
        options = self.visit(ctx.compactOptions()) if ctx.compactOptions() else []
        return ast.MapField(
            name=name,
            number=number,
            key_type=key_type,
            value_type=value_type,
            options=options,
        )

    def visitGroupDecl(self, ctx: ProtobufParser.GroupDeclContext):
        name = self._getText(ctx.fieldName())
        number = int(self._getText(ctx.fieldNumber()))
        cardinality = None
        if fieldCardinality := ctx.fieldCardinality():
            if fieldCardinality.OPTIONAL():
                cardinality = ast.FieldCardinality.OPTIONAL
            elif fieldCardinality.REQUIRED():
                cardinality = ast.FieldCardinality.REQUIRED
            elif fieldCardinality.REPEATED():
                cardinality = ast.FieldCardinality.REPEATED
        elements = [self.visit(child) for child in ctx.messageElement()]
        return ast.Group(
            name=name,
            number=number,
            cardinality=cardinality,
            elements=elements,
        )

    def visitOneofDecl(self, ctx: ProtobufParser.OneofDeclContext):
        name = self._getText(ctx.oneofName())
        elements = [self.visit(child) for child in ctx.oneofElement()]
        return ast.OneOf(name=name, elements=elements)

    def visitExtensionRangeDecl(self, ctx: ProtobufParser.ExtensionRangeDeclContext):
        ranges = [self._getText(child) for child in ctx.tagRanges().tagRange()]
        options = self.visit(ctx.compactOptions()) if ctx.compactOptions() else []
        return ast.ExtensionRange(ranges=ranges, options=options)

    def visitMessageReservedDecl(self, ctx: ProtobufParser.MessageReservedDeclContext):
        ranges = (
            [self._getText(child) for child in ctx.tagRanges().tagRange()]
            if ctx.tagRanges()
            else []
        )
        names = (
            [self._getText(child) for child in ctx.names().stringLiteral()]
            if ctx.names()
            else []
        )
        return ast.Reserved(ranges=ranges, names=names)

    def visitEnumDecl(self, ctx: ProtobufParser.EnumDeclContext):
        name = self._getText(ctx.enumName())
        elements = [self.visit(child) for child in ctx.enumElement()]
        return ast.Enum(name=name, elements=elements)

    def visitEnumValueDecl(self, ctx: ProtobufParser.EnumValueDeclContext):
        name = self._getText(ctx.enumValueName())
        number_text = self._getText(ctx.enumValueNumber())
        if number_text.lower().startswith("0x"):
            number = int(number_text, 16)
        else:
            number = int(number_text)
        options = self.visit(ctx.compactOptions()) if ctx.compactOptions() else []
        return ast.EnumValue(name=name, number=number, options=options)

    def visitEnumReservedDecl(self, ctx: ProtobufParser.EnumReservedDeclContext):
        ranges = (
            [self._getText(child) for child in ctx.enumValueRanges().enumValueRange()]
            if ctx.enumValueRanges()
            else []
        )
        names = (
            [self._getText(child) for child in ctx.names().stringLiteral()]
            if ctx.names()
            else []
        )
        return ast.EnumReserved(ranges=ranges, names=names)

    def visitExtensionDecl(self, ctx: ProtobufParser.ExtensionDeclContext):
        typeName = self._getText(ctx.extendedMessage())
        elements = [self.visit(child) for child in ctx.extensionElement()]
        return ast.Extension(typeName=typeName, elements=elements)

    def visitServiceDecl(self, ctx: ProtobufParser.ServiceDeclContext):
        name = self._getText(ctx.serviceName())
        elements = [self.visit(child) for child in ctx.serviceElement()]
        return ast.Service(name=name, elements=elements)

    def visitServiceElement(self, ctx: ProtobufParser.ServiceElementContext):
        if methodDecl := ctx.methodDecl():
            return self.visit(methodDecl)
        elif optionDecl := ctx.optionDecl():
            return self.visit(optionDecl)
        elif commentDecl := ctx.commentDecl():
            return self.visit(commentDecl)
        else:
            raise AttributeError("invalid service element")

    def visitMethodDecl(self, ctx: ProtobufParser.MethodDeclContext):
        name = self._getText(ctx.methodName())
        input_type = self.visit(ctx.inputType())
        output_type = self.visit(ctx.outputType())
        elements = [self.visit(child) for child in ctx.methodElement()]
        return ast.Method(
            name=name,
            input_type=input_type,
            output_type=output_type,
            elements=elements,
        )

    def visitInputType(self, ctx: ProtobufParser.InputTypeContext):
        return self.visit(ctx.messageType())

    def visitOutputType(self, ctx: ProtobufParser.OutputTypeContext):
        return self.visit(ctx.messageType())

    def visitMessageType(self, ctx: ProtobufParser.MessageTypeContext):
        name = self._getText(ctx.methodDeclTypeName())
        stream = ctx.STREAM() is not None
        return ast.MessageType(type=name, stream=stream)

    def visitMethodElement(self, ctx: ProtobufParser.MethodElementContext):
        if optionDecl := ctx.optionDecl():
            return self.visit(optionDecl)
        elif commentDecl := ctx.commentDecl():
            return self.visit(commentDecl)
        else:
            raise AttributeError("invalid method element")

    # ctx: ParserRuleContext, but ANTLR generates untyped code
    def _getText(self, ctx: Any, stripQuotes: bool = True):
        token_source = (
            ctx.start.getTokenSource()
        )  # pyright: ignore [reportGeneralTypeIssues]
        input_stream = token_source.inputStream
        start, stop = (
            ctx.start.start,
            ctx.stop.stop,
        )  # pyright: ignore [reportGeneralTypeIssues]
        text = input_stream.getText(start, stop)
        return text.strip('"') if stripQuotes else text


class Parser:
    def parse(self, text: str) -> ast.File:
        input_stream = InputStream(text)
        lexer = ProtobufLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = ProtobufParser(token_stream)
        parse_tree = parser.file_()
        visitor = ASTConstructor()
        return visitor.visit(parse_tree)  # pyright: ignore [reportGeneralTypeIssues]
