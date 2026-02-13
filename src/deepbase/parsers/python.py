# src/deepbase/parsers/python.py
import ast
import os
from .interface import LanguageParser

def _extract_module_comments(source: str) -> str:
    """
    Estrae i commenti # e la docstring di modulo dalle prime righe del sorgente.
    """
    lines = []
    in_docstring = False
    docstring_char = None
    source_lines = source.splitlines()

    for line in source_lines:
        stripped = line.strip()

        # Riga vuota: la includiamo solo se siamo già dentro i commenti iniziali
        if not stripped:
            if lines:
                lines.append("")
            continue

        # Commenti # semplici
        if stripped.startswith("#") and not in_docstring:
            lines.append(line.rstrip())
            continue

        # Inizio docstring di modulo (""" o ''')
        if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
            docstring_char = stripped[:3]
            in_docstring = True
            lines.append(line.rstrip())
            # Docstring su singola riga
            rest = stripped[3:]
            if rest.endswith(docstring_char) and len(rest) >= 3:
                in_docstring = False
            continue

        if in_docstring:
            lines.append(line.rstrip())
            if stripped.endswith(docstring_char):
                in_docstring = False
            continue

        # Qualsiasi altra cosa: fine dell'header
        break

    # Rimuovi trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines)


class LightVisitor(ast.NodeVisitor):
    """
    Visita l'AST e produce le firme dei metodi/funzioni Python.
    """

    def __init__(self):
        self.output = []
        self.indent_level = 0

    def _log(self, text):
        indent = "    " * self.indent_level
        self.output.append(f"{indent}{text}")

    def visit_ClassDef(self, node):
        self._log(f"class {node.name}:")
        self.indent_level += 1

        # Docstring della classe (prima riga)
        docstring = ast.get_docstring(node)
        if docstring:
            first_line = docstring.split('\n')[0].strip()
            self._log(f'"""{first_line}"""')

        self.generic_visit(node)
        self.indent_level -= 1

    def visit_FunctionDef(self, node):
        self._emit_signature(node, is_async=False)

    def visit_AsyncFunctionDef(self, node):
        self._emit_signature(node, is_async=True)

    def _emit_signature(self, node, is_async: bool):
        prefix = "async " if is_async else ""

        # --- Argomenti con annotazioni di tipo ---
        args_parts = []
        all_args = node.args.args
        defaults = node.args.defaults
        defaults_offset = len(all_args) - len(defaults)

        for i, arg in enumerate(all_args):
            arg_str = arg.arg
            if arg.annotation:
                try:
                    arg_str += f": {ast.unparse(arg.annotation)}"
                except Exception:
                    # Fallback per vecchie versioni python o AST complessi
                    pass
            default_idx = i - defaults_offset
            if default_idx >= 0:
                try:
                    default_val = ast.unparse(defaults[default_idx])
                    arg_str += f" = {default_val}"
                except Exception:
                    arg_str += " = ..."
            args_parts.append(arg_str)

        # *args
        if node.args.vararg:
            va = node.args.vararg
            va_str = f"*{va.arg}"
            if va.annotation:
                try:
                    va_str += f": {ast.unparse(va.annotation)}"
                except Exception:
                    pass
            args_parts.append(va_str)

        # keyword-only args
        kwonly_defaults = {
            i: node.args.kw_defaults[i]
            for i in range(len(node.args.kwonlyargs))
            if node.args.kw_defaults[i] is not None
        }
        for i, kwarg in enumerate(node.args.kwonlyargs):
            kw_str = kwarg.arg
            if kwarg.annotation:
                try:
                    kw_str += f": {ast.unparse(kwarg.annotation)}"
                except Exception:
                    pass
            if i in kwonly_defaults:
                try:
                    kw_str += f" = {ast.unparse(kwonly_defaults[i])}"
                except Exception:
                    kw_str += " = ..."
            args_parts.append(kw_str)

        # **kwargs
        if node.args.kwarg:
            kwa = node.args.kwarg
            kwa_str = f"**{kwa.arg}"
            if kwa.annotation:
                try:
                    kwa_str += f": {ast.unparse(kwa.annotation)}"
                except Exception:
                    pass
            args_parts.append(kwa_str)

        args_str = ", ".join(args_parts)

        # --- Tipo di ritorno ---
        ret_anno = ""
        if node.returns:
            try:
                ret_anno = f" -> {ast.unparse(node.returns)}"
            except Exception:
                pass

        self._log(f"{prefix}def {node.name}({args_str}){ret_anno}: ...")

        # Docstring della funzione (prima riga)
        docstring = ast.get_docstring(node)
        if docstring:
            first_line = docstring.split('\n')[0].strip()
            self.indent_level += 1
            self._log(f'"""{first_line}"""')
            self.indent_level -= 1

    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit(child)


class PythonParser(LanguageParser):
    def parse(self, content: str, file_path: str) -> str:
        filename = os.path.basename(file_path)
        try:
            tree = ast.parse(content)
            visitor = LightVisitor()
            visitor.visit(tree)
            signatures = "\n".join(visitor.output)

            # Prepend commenti/docstring iniziali del modulo
            module_header = _extract_module_comments(content)
            
            parts = []
            if module_header:
                parts.append(module_header)
            if signatures:
                parts.append(signatures)
                
            result = "\n\n".join(parts)
            return result.strip() or f"(No functions or classes found in {filename})"
        except SyntaxError:
            return f"(Syntax Error parsing {filename})"
        except Exception as e:
            return f"(Error parsing Python file: {e})"