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
	return (T, x, x, x, x, x, x, x, x, x, x), (x, T, T, T, T, T, T, T, T, T, T)


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
		self.D()

	def A(self) -> None:
		if False:
			self.Get()
		elif self.StartOf(1):
			pass
		else:
			self.SynErr(11)
		self.Get()

	def B(self) -> None:
		if False:
			self.Get()
		elif self.StartOf(1):
			self.Get()
		else:
			self.SynErr(12)

	def C(self) -> None:
		while False:
			self.Get()
		self.Get()

	def D(self) -> None:
		if False:
			self.Get()
		self.Get()

	set = _generateSet()
	errorMessages = "EOF expected", "a expected", "b expected", "c expected", "d expected", "e expected", "f expected", "g expected", "h expected", "i expected", "??? expected", "invalid A", "invalid B"
