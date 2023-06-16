parser grammar ProtobufParser;

options {
	tokenVocab = ProtobufLexer;
}

file: BYTE_ORDER_MARK? syntaxDecl? fileElement* EOF;

fileElement: importDecl |
               packageDecl |
               optionDecl |
               messageDecl |
               enumDecl |
               extensionDecl |
               serviceDecl |
               emptyDecl;

syntaxDecl: SYNTAX EQUALS syntaxLevel SEMICOLON;

syntaxLevel: stringLiteral;

stringLiteral: STRING_LITERAL+;

emptyDecl: SEMICOLON;

packageDecl: PACKAGE packageName SEMICOLON;

packageName: qualifiedIdentifier;

importDecl: IMPORT ( WEAK | PUBLIC )? importedFileName SEMICOLON;

importedFileName: stringLiteral;

typeName: DOT? qualifiedIdentifier;

qualifiedIdentifier: identifier ( DOT identifier )*;

fieldDeclTypeName: fieldDeclIdentifier ( DOT qualifiedIdentifier )? |
                    fullyQualifiedIdentifier;

messageFieldDeclTypeName: messageFieldDeclIdentifier ( DOT qualifiedIdentifier )? |
                            fullyQualifiedIdentifier;

extensionFieldDeclTypeName: extensionFieldDeclIdentifier ( DOT qualifiedIdentifier )? |
                            fullyQualifiedIdentifier;

oneofFieldDeclTypeName: oneofFieldDeclIdentifier ( DOT qualifiedIdentifier )? |
                        fullyQualifiedIdentifier;

methodDeclTypeName: methodDeclIdentifier ( DOT qualifiedIdentifier )? |
                    fullyQualifiedIdentifier;

fieldDeclIdentifier: alwaysIdent  | MESSAGE    | ENUM     | ONEOF  |
                        RESERVED  | EXTENSIONS | EXTEND   | OPTION |
                        OPTIONAL  | REQUIRED   | REPEATED | STREAM;

messageFieldDeclIdentifier: alwaysIdent | STREAM;

extensionFieldDeclIdentifier: alwaysIdent | MESSAGE  | ENUM       |
                                ONEOF     | RESERVED | EXTENSIONS |
                                EXTEND    | OPTION   | STREAM;

oneofFieldDeclIdentifier: alwaysIdent | MESSAGE    | ENUM     | ONEOF  |
                            RESERVED  | EXTENSIONS | EXTEND   | OPTION |
                            OPTIONAL  | REQUIRED   | REPEATED | GROUP;

methodDeclIdentifier: alwaysIdent | MESSAGE    | ENUM     | ONEOF  |
                        RESERVED  | EXTENSIONS | EXTEND   | OPTION |
                        OPTIONAL  | REQUIRED   | REPEATED | GROUP;

fullyQualifiedIdentifier: DOT qualifiedIdentifier;

optionDecl: OPTION optionName EQUALS optionValue SEMICOLON;

compactOptions: L_BRACKET compactOption ( COMMA compactOption )* R_BRACKET;

compactOption : optionName EQUALS optionValue;

optionName: ( identifier | L_PAREN typeName R_PAREN ) ( DOT optionName )*;

optionValue: scalarValue | messageLiteralWithBraces;

scalarValue : stringLiteral | uintLiteral | intLiteral | floatLiteral | identifier;

uintLiteral : PLUS? INT_LITERAL;

intLiteral  : MINUS INT_LITERAL;

floatLiteral: ( MINUS | PLUS )? (FLOAT_LITERAL | INF );

messageLiteralWithBraces: L_BRACE messageTextFormat R_BRACE;

messageTextFormat: ( messageLiteralField ( COMMA | SEMICOLON )? )*;

messageLiteralField: messageLiteralFieldName COLON value |
                       messageLiteralFieldName messageValue;

messageLiteralFieldName: fieldName |
                           L_BRACKET specialFieldName R_BRACKET;

specialFieldName       : extensionFieldName | typeURL;

extensionFieldName     : qualifiedIdentifier;

typeURL                : qualifiedIdentifier SLASH qualifiedIdentifier;

value         : scalarValue | messageLiteral | listLiteral;

messageValue  : messageLiteral | listOfMessagesLiteral;

messageLiteral: messageLiteralWithBraces |
                  L_ANGLE messageTextFormat R_ANGLE;

listLiteral: L_BRACKET ( listElement ( COMMA listElement )* )? R_BRACKET;

listElement: scalarValue | messageLiteral;

listOfMessagesLiteral: L_BRACKET ( messageLiteral ( COMMA messageLiteral )* )? R_BRACKET;

messageDecl: MESSAGE messageName L_BRACE messageElement* R_BRACE;

messageName   : identifier;

messageElement: messageFieldDecl |
                  groupDecl |
                  oneofDecl |
                  optionDecl |
                  extensionRangeDecl |
                  messageReservedDecl |
                  messageDecl |
                  enumDecl |
                  extensionDecl |
                  mapFieldDecl |
                  emptyDecl;

messageFieldDecl: fieldDeclWithCardinality |
                  messageFieldDeclTypeName fieldName EQUALS fieldNumber
                       compactOptions? SEMICOLON;

fieldDeclWithCardinality: fieldCardinality fieldDeclTypeName fieldName
                          EQUALS fieldNumber compactOptions? SEMICOLON;

fieldCardinality: REQUIRED | OPTIONAL | REPEATED;

fieldName       : identifier;

fieldNumber     : INT_LITERAL;

mapFieldDecl: mapType fieldName EQUALS fieldNumber compactOptions? SEMICOLON;

mapType   : MAP L_ANGLE mapKeyType COMMA typeName R_ANGLE;

mapKeyType:   INT32   | INT64   | UINT32   | UINT64   | SINT32 | SINT64 |
              FIXED32 | FIXED64 | SFIXED32 | SFIXED64 | BOOL   | STRING;

groupDecl: fieldCardinality? GROUP fieldName EQUALS fieldNumber
             compactOptions? L_BRACE messageElement* R_BRACE;

oneofDecl: ONEOF oneofName L_BRACE oneofElement* R_BRACE;

oneofName   : identifier;

oneofElement: optionDecl |
                oneofFieldDecl |
                oneofGroupDecl;

oneofFieldDecl: oneofFieldDeclTypeName fieldName EQUALS fieldNumber
                  compactOptions? SEMICOLON;

oneofGroupDecl: GROUP fieldName EQUALS fieldNumber
                  compactOptions? L_BRACE messageElement* R_BRACE;

extensionRangeDecl: EXTENSIONS tagRanges compactOptions? SEMICOLON;

tagRanges    : tagRange ( COMMA tagRange )*;

tagRange     : tagRangeStart ( TO tagRangeEnd )?;

tagRangeStart: fieldNumber;

tagRangeEnd  : fieldNumber | MAX;

messageReservedDecl: RESERVED ( tagRanges | names ) SEMICOLON;

names: stringLiteral ( COMMA stringLiteral )*;

enumDecl: ENUM enumName L_BRACE enumElement* R_BRACE;

enumName   : identifier;

enumElement: optionDecl |
               enumValueDecl |
               enumReservedDecl |
               emptyDecl;

enumValueDecl: enumValueName EQUALS enumValueNumber compactOptions? SEMICOLON;

enumValueName  : identifier;

enumValueNumber: MINUS? INT_LITERAL;

enumReservedDecl: RESERVED ( enumValueRanges | names ) SEMICOLON;

enumValueRanges    : enumValueRange ( COMMA enumValueRange )*;

enumValueRange     : enumValueRangeStart ( TO enumValueRangeEnd )?;

enumValueRangeStart: enumValueNumber;

enumValueRangeEnd  : enumValueNumber | MAX;

extensionDecl: EXTEND extendedMessage L_BRACE extensionElement* R_BRACE;

extendedMessage : typeName;

extensionElement: extensionFieldDecl |
                    groupDecl;

extensionFieldDecl: fieldDeclWithCardinality |
                    extensionFieldDeclTypeName fieldName EQUALS fieldNumber
                       compactOptions? SEMICOLON;

serviceDecl: SERVICE serviceName L_BRACE serviceElement* R_BRACE;

serviceName   : identifier;

serviceElement: optionDecl |
                  methodDecl |
                  emptyDecl;

methodDecl: RPC methodName inputType RETURNS outputType SEMICOLON |
              RPC methodName inputType RETURNS outputType L_BRACE methodElement* R_BRACE;

methodName   : identifier;

inputType    : messageType;

outputType   : messageType;

methodElement: optionDecl |
                emptyDecl;

messageType: L_PAREN STREAM? methodDeclTypeName R_PAREN;

identifier: alwaysIdent | sometimesIdent;

alwaysIdent: IDENTIFIER
    | SYNTAX
    | IMPORT
    | WEAK
    | PUBLIC
    | PACKAGE
    | INF
    | BOOL
    | STRING
    | BYTES
    | FLOAT
    | DOUBLE
    | INT32
    | INT64
    | UINT32
    | UINT64
    | SINT32
    | SINT64
    | FIXED32
    | FIXED64
    | SFIXED32
    | SFIXED64
    | MAP
    | TO
    | MAX
    | SERVICE
    | RPC
    | RETURNS;

sometimesIdent: MESSAGE
    | ENUM
    | ONEOF
    | RESERVED
    | EXTENSIONS
    | EXTEND
    | OPTION
    | OPTIONAL
    | REQUIRED
    | REPEATED
    | GROUP
    | STREAM;
