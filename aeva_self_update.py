# ~/aeva/self_update.py

import os
import datetime
import ast
import hashlib


class AevaSelfUpdate:
    def __init__(self, brain):
        self.brain = brain
        self.update_log = "update_log.txt"

    def _module_path(self, module_name):
        return f"{module_name}.py" if not module_name.endswith(
            ".py") else module_name

    def _secure_hash(self, code):
        return hashlib.sha256(code.encode()).hexdigest()

    def _log_update(self, module, action, content=None):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "module": module,
            "action": action,
            "user": self.brain.config.environment["user"],
            "hash": self._secure_hash(content or ""),
        }
        with open(self.update_log, "a") as f:
            f.write(f"{log_entry}\n")
        self.brain.log(f"[SelfUpdate] {action} logged for {module}")

    def rewrite_module(self, module_name, intent_description, patch_code):
        if self.brain.neurolock.lock_state:
            return "[SelfUpdate] Blocked: NeuroLock is engaged."

        path = self._module_path(module_name)
        if not os.path.exists(path):
            return f"[SelfUpdate] Module not found: {path}"

        try:
            with open(path, "r") as f:
                original_code = f.read()

            # Syntax validation before applying
            compile(patch_code, path, 'exec')  # raises SyntaxError if bad
            full_code = original_code + "\n\n# -- AEVA PATCH START --\n"
            full_code += f"# INTENT: {intent_description}\n"
            full_code += patch_code
            full_code += "\n# -- AEVA PATCH END --\n"

            with open(path, "w") as f:
                f.write(full_code)

            self._log_update(module_name, "rewrite", patch_code)
            return f"[SelfUpdate] {module_name} updated successfully."
        except SyntaxError as e:
            return f"[SelfUpdate] Syntax error: {e}"
        except Exception as e:
            return f"[SelfUpdate] Failed: {str(e)}"

    def validate_module(self, module_name):
        path = self._module_path(module_name)
        try:
            with open(path, "r") as f:
                code = f.read()
            compile(code, path, "exec")
            return "[SelfUpdate] Syntax OK."
        except SyntaxError as e:
            return f"[SelfUpdate] Syntax error: {e}"

    def review_code(self, module_name):
        path = self._module_path(module_name)
        if not os.path.exists(path):
            return f"[SelfUpdate] File not found: {path}"

        try:
            with open(path, "r") as f:
                code = f.read()
            tree = ast.parse(code)

            issues = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module == "*":
                    issues.append("Avoid wildcard imports (from ... import *)")
                if isinstance(node, ast.FunctionDef) and len(node.body) > 50:
                    issues.append(
                        f"Function '{
                            node.name}' is very long. Consider refactoring.")

            if not issues:
                return ["[SelfUpdate] Code appears clean."]
            return issues

        except Exception as e:
            return [f"[SelfUpdate] Review failed: {str(e)}"]

    def backup_module(self, module_name):
        path = self._module_path(module_name)
        if not os.path.exists(path):
            return f"[SelfUpdate] Cannot backup — file not found: {path}"

        backup_path = f"{path}.bak_{
            datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        with open(path, "r") as f:
            code = f.read()
        with open(backup_path, "w") as f:
            f.write(code)

        self._log_update(module_name, "backup", code)
        return f"[SelfUpdate] Backup created: {backup_path}"

    def rollback(self, module_name):
        backups = [f for f in os.listdir(".") if f.startswith(
            module_name) and f.endswith(".py") and ".bak_" in f]
        if not backups:
            return "[SelfUpdate] No backups found."

        latest_backup = sorted(backups)[-1]
        with open(latest_backup, "r") as f:
            code = f.read()

        with open(self._module_path(module_name), "w") as f:
            f.write(code)

        self._log_update(module_name, "rollback", code)
        return f"[SelfUpdate] Rolled back to: {latest_backup}"
