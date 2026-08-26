import sys
import io
import traceback

def execute_and_auto_debug(python_code: str) -> dict:
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    local_scope = {}
    try:
        exec(python_code, globals(), local_scope)
        sys.stdout = old_stdout
        return {
            "status": "success",
            "output": redirected_output.getvalue(),
            "variables": {k: str(v) for k, v in local_scope.items() if not k.startswith("__")}
        }
    except Exception as e:
        sys.stdout = old_stdout
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc(),
            "instruction": "حلل سبب الخطأ واكتب الكود المصحح وأعد تشغيله."
        }