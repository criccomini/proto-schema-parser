lexer grammar ProtobufLexer;

// discard whitespace and comment tokens
WS  :   [ \t\r\n\u000C]+ -> channel(HIDDEN);
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);
COMMENT: '/*' .*? '*/' -> channel(HIDDEN);

// character classes
fragment LETTER: [A-Za-z_];
fragment DECIMAL_DIGIT: [0-9];
fragment OCTAL_DIGIT: [0-7];
fragment HEX_DIGIT: [0-9A-Fa-f];

BYTE_ORDER_MARK: '\uFEFF';

// identifiers and keywords
SYNTAX: 'syntax';
IMPORT: 'import';
WEAK: 'weak';
PUBLIC: 'public';
PACKAGE: 'package';
OPTION: 'option';
INF: 'inf';
REPEATED: 'repeated';
OPTIONAL: 'optional';
REQUIRED: 'required';
BOOL: 'bool';
STRING: 'string';
BYTES: 'bytes';
FLOAT: 'float';
DOUBLE: 'double';
INT32: 'int32';
INT64: 'int64';
UINT32: 'uint32';
UINT64: 'uint64';
SINT32: 'sint32';
SINT64: 'sint64';
FIXED32: 'fixed32';
FIXED64: 'fixed64';
SFIXED32: 'sfixed32';
SFIXED64: 'sfixed64';
GROUP: 'group';
ONEOF: 'oneof';
MAP: 'map';
EXTENSIONS: 'extensions';
TO: 'to';
MAX: 'max';
RESERVED: 'reserved';
ENUM: 'enum';
MESSAGE: 'message';
EXTEND: 'extend';
SERVICE: 'service';
RPC: 'rpc';
STREAM: 'stream';
RETURNS: 'returns';

IDENTIFIER: LETTER ( LETTER | DECIMAL_DIGIT )*;

// numeric literals
INT_LITERAL: DECIMAL_LITERAL | OCTAL_LITERAL | HEX_LITERAL;
fragment DECIMAL_LITERAL: [1-9] DECIMAL_DIGIT*;
fragment OCTAL_LITERAL: '0' OCTAL_DIGIT*;
fragment HEX_LITERAL: '0' ( 'x' | 'X' ) HEX_DIGIT+ ;

FLOAT_LITERAL: DECIMAL_DIGIT+ DOT DECIMAL_DIGIT* DECIMAL_EXPONENT? |
                DECIMAL_DIGIT+ DECIMAL_EXPONENT |
                DOT DECIMAL_DIGIT+ DECIMAL_EXPONENT?;
fragment DECIMAL_EXPONENT: ( 'e' | 'E' ) (PLUS | MINUS)? DECIMAL_DIGIT+;

// we can't do a two pass approach for identifying numeric literals, like the
// spec describes, but we can instead provide explicit tokens for *invalid*
// numeric literals, so we can still reject them (instead of incorrectly
// identifying input as a valid literal, no whitespace, and then another
// token).
INVALID_INT_LITERAL: INT_LITERAL ( LETTER | DOT );
INVALID_FLOAT_LITERAL: FLOAT_LITERAL ( LETTER | DOT );

// string literals
STRING_LITERAL: SINGLE_QUOTED_STRING_LITERAL | DOUBLE_QUOTED_STRING_LITERAL;

fragment SINGLE_QUOTED_STRING_LITERAL: '\'' ( ~[\n\u0000'\\] | RUNE_ESCAPE_SEQ )* '\'';
fragment DOUBLE_QUOTED_STRING_LITERAL: '"' ( ~[\n\u0000"\\] | RUNE_ESCAPE_SEQ )* '"';

fragment RUNE_ESCAPE_SEQ: SIMPLE_ESCAPE_SEQ | HEX_ESCAPE_SEQ | OCTAL_ESCAPE_SEQ | UNICODE_ESCAPE_SEQ;
fragment SIMPLE_ESCAPE_SEQ: '\\' ( 'a' | 'b' | 'f' | 'n' | 'r' | 't' | 'v' | '\\' | '\'' | '"' | '?' );
fragment HEX_ESCAPE_SEQ: '\\' ( 'x' | 'X' ) HEX_DIGIT HEX_DIGIT;
fragment OCTAL_ESCAPE_SEQ: '\\' OCTAL_DIGIT ( OCTAL_DIGIT OCTAL_DIGIT? )?;
fragment UNICODE_ESCAPE_SEQ: '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT |
                             '\\' 'U' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
                                      HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT;

// punctuation and operators
SEMICOLON: ';';
COMMA: ',';
DOT: '.';
SLASH: '/';
COLON: ':';
EQUALS: '=';
MINUS: '-';
PLUS: '+';
L_PAREN: '(';
R_PAREN: ')';
L_BRACE: '{';
R_BRACE: '}';
L_BRACKET: '[';
R_BRACKET: ']';
L_ANGLE: '<';
R_ANGLE: '>';
