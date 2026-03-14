import subprocess
from .gemini_service import GeminiService

class MDMService:
    def __init__(self):
        self.gemini = GeminiService()

    def execute_adb_command(self, command):
        try:
            if not command.startswith('adb'): command = f"adb {command}"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            return {"success": process.returncode == 0, "output": stdout, "error": stderr}
        except Exception as e:
            return {"success": False, "output": None, "error": str(e)}

    def diagnose_device(self):
        model = self.execute_adb_command("shell getprop ro.product.model")
        brand = self.execute_adb_command("shell getprop ro.product.brand")
        packages = self.execute_adb_command("shell pm list packages -f")
        return {
            "model": model.get("output", "").strip(),
            "brand": brand.get("output", "").strip(),
            "packages": packages.get("output", "").strip()
        }

    def remove_package(self, package_name):
        return self.execute_adb_command(f"shell pm uninstall --user 0 {package_name}")

    def ai_assisted_unlock(self, device_info, last_error):
        suggested_commands = self.gemini.get_unlock_commands(device_info, last_error)
        results = []
        for cmd in suggested_commands:
            results.append({"command": cmd, "result": self.execute_adb_command(cmd)})
        return results
