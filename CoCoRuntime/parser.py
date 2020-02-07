"""Parser.py -- ATG parser runtime"""

__copyright__ = """
Compiler Generator Coco/R,
Copyright (c) 1990, 2004 Hanspeter Moessenboeck, University of Linz
extended by M. Loeberbauer & A. Woess, Univ. of Linz
ported from Java to Python by Ronald Longo
improved and refactored by KOLANICH

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

As an exception, it is allowed to write an extension of Coco/R that is used as a plugin in non-free software.

If not otherwise stated, any source code generated by Coco/R (other than Coco/R itself) does not fall under the GNU General Public License.
"""  # pylint: disable=duplicate-code

import typing
from abc import ABC, abstractmethod

from .errors import Errors
from .scanner import Scanner, Token


class Parser(ABC):
	ENUM = None
	__main_production_name__ = None  # type: str
	__EOF_sym__ = None  # type: typing.Type["ScannerEnum"]

	@abstractmethod
	def pragmas(self):
		raise NotImplementedError

	set = None
	errorMessages = None
	minErrDist = 2

	# -->declarations

	def __init__(self) -> None:
		self.scanner = None
		self.token = None  # last recognized token
		self.la = None  # lookahead token
		self.genScanner = False
		self.tokenString = ""  # used in declarations of literal tokens
		self.noString = "-none-"  # used in declarations of literal tokens
		self.errDist = self.__class__.minErrDist
		self.errors = Errors()

	def getParsingPos(self) -> typing.Tuple[int, int]:
		return self.la.line, self.la.col

	def SynErr(self, errNum: int) -> None:
		if self.errDist >= self.__class__.minErrDist:
			line, col = self.getParsingPos()
			self.errors.storeError(line, col, self.__class__.errorMessages[errNum])

		self.errDist = 0

	def SemErr(self, msg: str) -> None:
		if self.errDist >= self.__class__.minErrDist:
			line, col = self.getParsingPos()
			self.errors.storeError(line, col, msg)

		self.errDist = 0

	def Warning(self, msg):
		if self.errDist >= self.__class__.minErrDist:
			self.errors.Warn(msg)

		self.errDist = 0

	@staticmethod
	def Successful():
		return self.errors.count == 0

	def LexString(self):
		return self.token.val

	def LookAheadString(self):
		return self.la.val

	def Get(self) -> None:
		while True:
			self.token = self.la
			self.la = self.scanner.Scan()
			if self.la.kind <= self.__class__.ENUM.maxT:
				self.errDist += 1
				break
			self.pragmas()
			self.la = self.token

	def Expect(self, n: "ScannerEnum") -> None:
		if self.la.kind == n:
			self.Get()
		else:
			self.SynErr(n)

	def StartOf(self, s: int) -> bool:
		return self._StartOf(s, self.la.kind)

	@classmethod
	def _StartOf(cls, s: int, kind: "ScannerEnum") -> bool:
		if kind >= 0:
			return cls.set[s][kind]
		return False

	def ExpectWeak(self, n: "ScannerEnum", follow: int) -> None:
		if self.la.kind == n:
			self.Get()
		else:
			self.SynErr(n)
			while not self.StartOf(follow):
				self.Get()

	def WeakSeparator(self, n: "ScannerEnum", syFol: int, repFol: int) -> bool:
		s = [False for i in range(self.__class__.ENUM.maxT + 1)]
		if self.la.kind == n:
			self.Get()
			return True

		if self.StartOf(repFol):
			return False

		for i in range(self.__class__.ENUM.maxT):
			s[i] = self._StartOf(syFol, i) or self._StartOf(repFol, i) or self._StartOf(0, i)
		self.SynErr(n)
		while not s[self.la.kind]:
			self.Get()
		return self.StartOf(syFol)

	@property
	def __main_production__(self) -> typing.Callable[[], None]:
		return getattr(self, self.__class__.__main_production_name__)

	def Parse(self, scanner: Scanner) -> None:
		self.scanner = scanner
		self.la = Token()
		self.la.val = ""
		self.Get()
		self.__main_production__()
		self.Expect(self.__class__.ENUM.EOF_SYM)
