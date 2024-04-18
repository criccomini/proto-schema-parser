from proto_schema_parser import ast


class Generator:
    def generate(self, file: ast.File) -> str:
        lines = []

        # Syntax
        if file.syntax:
            lines.append(f'syntax = "{file.syntax}";')

        # File Elements
        for element in file.file_elements:
            if isinstance(element, ast.Package):
                lines.append(f"package {element.name};")
            elif isinstance(element, ast.Import):
                modifier = ""
                if element.weak:
                    modifier = "weak "
                elif element.public:
                    modifier = "public "
                lines.append(f'import {modifier}"{element.name}";')
            elif isinstance(element, ast.Option):
                if isinstance(element.value, bool):
                    if element.value:
                        lines.append(f"option {element.name} = true;")
                    else:
                        lines.append(f"option {element.name} = false;")
                else:
                    lines.append(f'option {element.name} = "{element.value}";')
            elif isinstance(element, ast.Message):
                lines.append(self._generate_message(element))
            elif isinstance(element, ast.Enum):
                lines.append(self._generate_enum(element))
            elif isinstance(element, ast.Extension):
                lines.append(self._generate_extension(element))
            elif isinstance(element, ast.Service):
                lines.append(self._generate_service(element))
            elif isinstance(element, ast.Comment):
                lines.append(self._generate_comment(element))

        return "\n".join(lines)

    def _generate_message(self, message: ast.Message, indent_level: int = 0) -> str:
        lines = [f"{'  ' * indent_level}message {message.name} {{"]
        for element in message.elements:
            if isinstance(element, ast.Field):
                lines.append(self._generate_field(element, indent_level + 1))
            elif isinstance(element, ast.MapField):
                lines.append(self._generate_map_field(element, indent_level + 1))
            elif isinstance(element, ast.Group):
                lines.append(self._generate_group(element, indent_level + 1))
            elif isinstance(element, ast.OneOf):
                lines.append(self._generate_one_of(element, indent_level + 1))
            elif isinstance(element, ast.ExtensionRange):
                lines.append(self._generate_extension_range(element, indent_level + 1))
            elif isinstance(element, ast.Reserved):
                lines.append(self._generate_reserved(element, indent_level + 1))
            elif isinstance(element, ast.Option):
                lines.append(self._generate_option(element, indent_level + 1))
            elif isinstance(element, ast.Message):  # Nested Message
                lines.append(self._generate_message(element, indent_level + 1))
            elif isinstance(element, ast.Enum):  # Enum
                lines.append(self._generate_enum(element, indent_level + 1))
            elif isinstance(element, ast.Extension):  # Extension
                lines.append(self._generate_extension(element, indent_level + 1))
            elif isinstance(element, ast.Comment):
                lines.append(self._generate_comment(element, indent_level + 1))

        lines.append(f"{'  ' * indent_level}}}")
        return "\n".join(lines)

    def _generate_service(self, service: ast.Service, indent_level: int = 0) -> str:
        lines = [f"{'  ' * indent_level}service {service.name} {{"]
        for element in service.elements:
            if isinstance(element, ast.Method):
                lines.append(self._generate_method(element, indent_level + 1))
            elif isinstance(element, ast.Option):
                lines.append(self._generate_option(element, indent_level + 1))
            elif isinstance(element, ast.Comment):
                lines.append(self._generate_comment(element, indent_level + 1))
        lines.append(f"{'  ' * indent_level}}}")
        return "\n".join(lines)

    def _generate_comment(self, comment: ast.Comment, indent_level: int = 0) -> str:
        lines = [f"{'  ' * indent_level}{comment.text}"]
        return "\n".join(lines)

    def _generate_method(self, method: ast.Method, indent_level: int = 0) -> str:
        input_type_str = self._generate_message_type(method.input_type)
        output_type_str = self._generate_message_type(method.output_type)

        has_options = any(
            isinstance(element, ast.Option) for element in method.elements
        )
        lines = [
            f"{'  ' * indent_level}rpc {method.name} ({input_type_str}) returns ({output_type_str}){'{' if has_options else ';'}"
        ]
        if has_options:
            for element in method.elements:
                if isinstance(element, ast.Option):
                    lines.append(self._generate_option(element, indent_level + 1))
                elif isinstance(element, ast.Comment):
                    lines.append(self._generate_comment(element, indent_level + 1))
            lines.append(f"{'  ' * indent_level}}}")
        return "\n".join(lines)

    def _generate_message_type(self, message_type: ast.MessageType) -> str:
        stream = "stream " if message_type.stream else ""
        return f"{stream}{message_type.type}"

    def _generate_field(self, field: ast.Field, indent_level: int = 0) -> str:
        cardinality = ""
        if field.cardinality:
            cardinality = f"{field.cardinality.value.lower()} "

        options = ""
        if field.options:
            options = " ["
            options += ", ".join(f'{opt.name} = "{opt.value}"' for opt in field.options)
            options += "]"

        return f"{'  ' * indent_level}{cardinality}{field.type} {field.name} = {field.number}{options};"

    def _generate_map_field(
        self, map_field: ast.MapField, indent_level: int = 0
    ) -> str:
        return f"{'  ' * indent_level}map<{map_field.key_type}, {map_field.value_type}> {map_field.name} = {map_field.number};"

    def _generate_group(self, group: ast.Group, indent_level: int = 0) -> str:
        lines = [f"{'  ' * indent_level}group {group.name} = {group.number} {{"]
        for element in group.elements:
            if isinstance(element, ast.Field):
                lines.append(self._generate_field(element, indent_level + 1))
            elif isinstance(element, ast.Option):
                lines.append(self._generate_option(element, indent_level + 1))
        lines.append(f"{'  ' * indent_level}}}")
        return "\n".join(lines)

    def _generate_one_of(self, one_of: ast.OneOf, indent_level: int = 0) -> str:
        lines = [f"{'  ' * indent_level}oneof {one_of.name} {{"]
        for element in one_of.elements:
            if isinstance(element, ast.Field):
                lines.append(self._generate_field(element, indent_level + 1))
            elif isinstance(element, ast.Option):
                lines.append(self._generate_option(element, indent_level + 1))
            elif isinstance(element, ast.Comment):
                lines.append(self._generate_comment(element, indent_level + 1))
        lines.append(f"{'  ' * indent_level}}}")
        return "\n".join(lines)

    def _generate_option(self, option: ast.Option, indent_level: int = 0) -> str:
        return f"{'  ' * indent_level}option {option.name} = \"{option.value}\";"

    def _generate_extension(
        self, extension: ast.Extension, indent_level: int = 0
    ) -> str:
        lines = [f"{'  ' * indent_level}extend {extension.typeName} {{"]
        for element in extension.elements:
            if isinstance(element, ast.Field):
                lines.append(self._generate_field(element, indent_level + 1))
            elif isinstance(element, ast.Group):
                lines.append(self._generate_group(element, indent_level + 1))
            elif isinstance(element, ast.Comment):
                lines.append(self._generate_comment(element, indent_level + 1))
        lines.append(f"{'  ' * indent_level}}}")
        return "\n".join(lines)

    def _generate_enum(self, enum: ast.Enum, indent_level: int = 0) -> str:
        lines = [f"{'  ' * indent_level}enum {enum.name} {{"]
        for element in enum.elements:
            if isinstance(element, ast.EnumValue):
                lines.append(
                    f"{'  ' * (indent_level + 1)}{element.name} = {element.number};"
                )
            elif isinstance(element, ast.EnumReserved):
                lines.append(self._generate_enum_reserved(element, indent_level + 1))
            elif isinstance(element, ast.Option):
                lines.append(self._generate_option(element, indent_level + 1))
            elif isinstance(element, ast.Comment):
                lines.append(self._generate_comment(element, indent_level + 1))
        lines.append(f"{'  ' * indent_level}}}")
        return "\n".join(lines)

    def _generate_enum_reserved(
        self, reserved: ast.EnumReserved, indent_level: int = 0
    ) -> str:
        ranges = ", ".join(reserved.ranges)
        names = ", ".join(reserved.names)
        return f"{'  ' * indent_level}reserved {ranges}, {names};"

    def _generate_extension_range(
        self, extension_range: ast.ExtensionRange, indent_level: int = 0
    ) -> str:
        ranges = ", ".join(extension_range.ranges)
        return f"{'  ' * indent_level}extensions {ranges};"

    def _generate_reserved(self, reserved: ast.Reserved, indent_level: int = 0) -> str:
        ranges = ", ".join(reserved.ranges)
        names = ", ".join(reserved.names)
        return f"{'  ' * indent_level}reserved {ranges}, {names};"

    @staticmethod
    def _indent(line: str, indent_level: int = 0) -> str:
        return f"{'  ' * indent_level}{line}"
