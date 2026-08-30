from module import Module
import requests

class SensitiveFileCheck(Module):
    
        CHECK_PATHS = ["/.env", "/.git/config", "/.git/HEAD", "/backup.zip", "/backup.tar.gz", "/db.sql", "/database.sql", "/config.php", "/config.json", "/web.config", "/error.log", "/debug.log", "/phpinfo.php", "/server-status", "/admin/", "/administrator/", "/phpmyadmin/", "/swagger/", "/api-docs/", "/storage/logs/"]

        def run(self) -> dict:
                findings = []
                
                try:
                        dummy_response = requests.get(self.target + "/totally_not_a_real_page", timeout=self.timeout)
                        not_found_page_len = len(dummy_response.text)
                except requests.exceptions.RequestException as e:
                        return {"target": self.target, "plugin": "sensitive_file_check", "findings": [{"description": f"Request failed: {e}", "severity": "error"}]}
                for path in self.CHECK_PATHS:
                    try:
                        response = requests.get(self.target + path, timeout=self.timeout)
                        if response.status_code == 200 and len(response.text) != not_found_page_len:
                            findings.append({"description": f"{path} is accessible", "severity": "medium"})
                    except requests.exceptions.RequestException:
                        pass
                return {"target": self.target, "plugin": "sensitive_file_check", "findings": findings}

