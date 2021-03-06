__copyright__ = """
If not otherwise stated, any source code generated by Coco/R (other than Coco/R itself) does not fall under the GNU General Public License.
"""
import typing
from functools import wraps
from CoCoRuntime.parser import Parser
from CoCoRuntime.scanner import Position
from .Scanner import ScannerEnum


def _generateSet() -> typing.Tuple[typing.Tuple[bool, ...], ...]:
	T = True
	x = False
	return ((T, x, x, x, x, x, x, x),)


class MyParser(Parser):
	__slots__ = ()

	@wraps(Parser.__init__)
	def __init__(self, *args, **kwargs):
		"""This ctor is mandatory, don't delete it: otherwise self.__class__.ENUM will be None"""
		super().__init__(*args, **kwargs)

	ENUM = ScannerEnum
	__main_production_name__ = "Test"
	__EOF_sym__ = ScannerEnum.EOF_SYM

	def pragmas(self) -> None:
		pass

	def Test(self) -> None:
		if self.la.kind == self.__class__.ENUM.a_Sym or self.la.kind == self.__class__.ENUM.b_Sym:
			if self.la.kind == self.__class__.ENUM.a_Sym:
				self.Get()
			else:
				pass
			self.Get()
		elif self.la.kind == self.__class__.ENUM.c_Sym or self.la.kind == self.__class__.ENUM.d_Sym or self.la.kind == self.__class__.ENUM.e_Sym:
			if self.la.kind == self.__class__.ENUM.c_Sym:
				self.Get()
			elif self.la.kind == self.__class__.ENUM.e_Sym:
				sem
			else:
				self.Get()
			self.Get()
		else:
			self.SynErr(8)

	set = _generateSet()
	errorMessages = "EOF expected", "a expected", "b expected", "c expected", "d expected", "e expected", "f expected", "??? expected", "invalid Test"
