__gpl_exception_generated__ = """
If not otherwise stated, any source code generated by Coco/R (other than Coco/R itself) does not fall under the GNU General Public License.
"""  # pylint: disable=duplicate-code

__copyright__ = """
Compiler Generator Coco/R,
Copyright (c) 1990, 2004 Hanspeter Moessenboeck, University of Linz
extended by M. Loeberbauer & A. Woess, Univ. of Linz
ported from Java to Python by Ronald Longo
improved and refactored by KOLANICH

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

As an exception, it is allowed to write an extension of Coco/R that is used as a plugin in non-free software.
""" + __gpl_exception_generated__  # pylint: disable=duplicate-code

import ast
from io import StringIO

from CoCoRuntime.errors import Errors

from .DFA import DFA
from .nodes import Node
from .Parser import MyParser as GeneratedParser
from .ParserGen import ParserGen
from .Scanner import MyScanner
from .ScannerGen import ScannerGen
from .symbols import SymTerminal
from .Tab import Tab
from .Trace import Trace


class MyParser(GeneratedParser):
	__slots__ = ("controller",)

	def __init__(self, controller: "Controller") -> None:
		super().__init__()
		self.controller = controller


class Result:
	__slots__ = ("scanner", "parser", "stats")

	def __init__(self) -> None:
		self.scanner = None
		self.parser = None
		self.stats = None


class Controller:
	"""The state that used to be global has moved here"""

	__slots__ = ("parserGen", "scannerGen", "dfa", "trace", "table", "errors", "preamble", "gramName", "grammarName1", "genScanner", "scanner", "graph")

	def __init__(self) -> None:
		super().__init__()
		self.parserGen = ParserGen()
		self.trace = Trace()
		self.dfa = DFA(trace=self.trace)
		self.scannerGen = ScannerGen(self.dfa)
		self.table = Tab()
		self.errors = Errors()
		self.preamble = None
		self.gramName = None
		self.grammarName1 = None
		self.genScanner = None
		self.scanner = None
		self.graph = None

	def parse(self, src: str) -> None:
		parser = MyParser(self)
		self.errors = Errors()
		self.scanner = MyScanner(src)
		parser.Parse(self.scanner)

	def generateScanner(self, useAnnotatedAssignments: bool = False) -> ast.Module:
		return self.scannerGen.WriteScanner(self.table, self.table.ddt.tokenNames, preamble=self.preamble, errors=self.errors, useAnnotatedAssignments=useAnnotatedAssignments)

	def generateParser(self, useAnnotatedAssignments: bool = False) -> ast.Module:
		return self.parserGen.WriteParser(self.table, self.table.ddt.tokenNames, preamble=self.preamble, useAnnotatedAssignments=useAnnotatedAssignments)

	def printStates(self) -> None:
		self.dfa.PrintStates()

	def writeStats(self) -> str:
		io = StringIO()
		self.parserGen.WriteStatistics(self.table, io)
		return io.getvalue()

	def printSymbolTable(self) -> None:
		self.table.PrintSymbolTable()

	def printNodes(self):
		Node.PrintNodes(self.graph, self.trace)

	def pipeline(self, useAnnotatedAssignments: bool = False) -> Result:
		res = Result()

		if self.gramName != self.grammarName1:
			self.errors.storeError(-1, -1, "name (" + repr(self.grammarName1) + ") does not match grammar name (" + repr(self.gramName) + ")")
		self.table.gramSy = self.table.findSymbol(self.gramName)
		if self.table.gramSy is None:
			self.errors.storeError(-1, -1, "missing production for grammar name (" + repr(self.gramName) + ")")
		else:
			sym = self.table.gramSy
			if sym.attrs:
				self.errors.storeError(-1, -1, "grammar symbol must not have attributes")
		self.table.noSym = SymTerminal(self.table, "???", 0, self.errors)  # noSym gets highest number
		self.table.SetupAnys()
		self.table.RenumberPragmas()
		if self.table.ddt.syntaxGraph:
			self.printNodes()
		if self.errors.count == 0:
			self.table.CompSymbolSets(self.errors)
			if self.table.ddt.crossReferences:
				self.table.XRef()
			if self.table.GrammarOk(self.errors):
				if not self.table.ddt.testOnly:
					if self.table.ddt.tokenNames:
						self.table.AssignNames(self.errors)
					res.parser = self.generateParser(useAnnotatedAssignments=useAnnotatedAssignments)
					if self.genScanner:
						res.scanner = self.generateScanner(useAnnotatedAssignments=useAnnotatedAssignments)
						if self.table.ddt.traceAutomaton:
							self.printStates()
				if self.table.ddt.statistics:
					res.stats = self.parserGen.WriteStatistics(self.table)
		if self.table.ddt.symbolTable:
			self.table.PrintSymbolTable()
		return res