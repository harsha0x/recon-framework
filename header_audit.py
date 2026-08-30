from module import Module
import requests


class HeaderAudit(Module):
	CHECK_HEADERS = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]

	def run(self) -> dict:
		findings = []
		try:
			response = requests.get(self.target, timeout=self.timeout)
		except requests.exceptions.RequestException as e:
			findings.append({"description": f"Request Failed {e}", "severity": "error"})
			return {"target": self.target, "plugin": "header_audit", "findings": findings}
			
		for header in self.CHECK_HEADERS:
			if header not in response.headers:
				findings.append({"description": f"{header} header not found", "severity": "medium"})


		return {"target": self.target, "plugin": "header_audit", "findings": findings}

