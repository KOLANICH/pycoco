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
	return (T, x, x, x, x, x, x, x, x, x, x), (T, x, x, T, x, x, x, x, x, x, x), (x, x, x, T, x, x, x, x, x, x, x), (x, x, x, x, T, x, x, x, x, x, x), (x, x, T, T, x, x, x, x, x, x, x)


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
		self.A()
		self.B()
		self.C()

	def A(self) -> None:
		self.Expect(self.__class__.ENUM.a_Sym)
		self.ExpectWeak(self.__class__.ENUM.b_Sym, 1)
		self.Expect(self.__class__.ENUM.c_Sym)

	def B(self) -> None:
		self.Expect(self.__class__.ENUM.a_Sym)
		while self.WeakSeparator(self.__class__.ENUM.b_Sym, 2, 3):
			self.Expect(self.__class__.ENUM.c_Sym)
		self.Expect(self.__class__.ENUM.d_Sym)

	def C(self) -> None:
		self.Expect(self.__class__.ENUM.a_Sym)
		while self.WeakSeparator(self.__class__.ENUM.b_Sym, 4, 2):
			pass
		self.Expect(self.__class__.ENUM.c_Sym)

	set = _generateSet()
	errorMessages = "EOF expected", "a expected", "b expected", "c expected", "d expected", "e expected", "f expected", "g expected", "h expected", "i expected", "??? expected"
