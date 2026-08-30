
from abc import ABC, abstractmethod 

class Module(ABC):
	def __init__(self, target, timeout=10):
		self.target = target
		self.timeout = timeout
		
	@abstractmethod
	def run(self) -> dict:
		pass
		
	
	def execute(self):
		result = self.run()
		if not self._is_valid(result):
			print(f"warning {self.__class__.__name__} returned a bad result, skipping")
			return None
		return result
	
	def _is_valid(self, result):
		return(
			isinstance(result, dict)
			and "target" in result
			and "plugin" in result
			and "findings" in result
		)
				
		
