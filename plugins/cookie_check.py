from module import Module
import requests

class CookieCheck(Module):
    cookies = ["secure", "HttpOnly","SameSite"]
    
    def run(self) -> dict:
        findings = []
        try:
            response = requests.get(self.target, timeout=self.timeout)
        except requests.RequestException as e:
            return {"target": self.target, "plugin": "cookie_check", "findings": [{"description": f"Error occurred while fetching target: {e}", "severity": "info"}]}

        set_cookie_headers = []
        all_cookies = response.history + [response]

        for r in all_cookies:
            cookies = r.raw.headers.get_all("Set-Cookie")
            if cookies:
                set_cookie_headers.extend(cookies)

        if not set_cookie_headers:
            return {"target": self.target, "plugin": "cookie_check", "findings": [{"description": "No Set-Cookie headers found", "severity": "info"}]}

        for set_cookie in set_cookie_headers:
            for cookie in self.cookies:
                if cookie.lower() not in set_cookie.lower():
                    findings.append({"description": f"Cookie {cookie} is missing", "severity": "high"})
                
        return {"target": self.target, "plugin": "cookie_check", "findings": findings}