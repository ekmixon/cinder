from __future__ import annotations

from ast import AST
from contextlib import nullcontext
from typing import Optional, Sequence, Union, TYPE_CHECKING

from ..visitor import ASTVisitor

if TYPE_CHECKING:
    from . import SymbolTable
    from .module_table import ModuleTable


class GenericVisitor(ASTVisitor):
    def __init__(self, module: ModuleTable) -> None:
        super().__init__()
        self.module = module
        self.module_name: str = module.name
        self.filename: str = module.filename
        self.symtable: SymbolTable = module.symtable

    def visit(self, node: Union[AST, Sequence[AST]], *args: object) -> Optional[object]:
        # if we have a sequence of nodes, don't catch TypedSyntaxError here;
        # walk_list will call us back with each individual node in turn and we
        # can catch errors and add node info then.
        ctx = (
            self.module.error_context(node) if isinstance(node, AST) else nullcontext()
        )
        with ctx:
            return super().visit(node, *args)

    def syntax_error(self, msg: str, node: AST) -> None:
        return self.symtable.error_sink.syntax_error(msg, self.filename, node)
