import sys
from importlib.abc import MetaPathFinder
import threading

class VataImportInterceptor(MetaPathFinder):
    """
    Enforced Import Interceptor for VATA Framework.
    Injected directly into sys.meta_path to catch unauthorized module loads
    at the interpreter level, eliminating voluntary bookkeeping bypasses.
    """
    def __init__(self):
        self._local = threading.local()

    @property
    def allowed_modules(self):
        if not hasattr(self._local, 'allowed'):
            self._local.allowed = set()
        return self._local.allowed

    def set_allowed_modules(self, modules_list):
        self._local.allowed = set(modules_list)

    def find_spec(self, fullname, path, target=None):
        # Always allow standard built-in core tracking layers if needed
        if not self.allowed_modules:
            return None
            
        # Check if the requested module or its parent package is permitted
        base_module = fullname.split('.')[0]
        if base_module not in self.allowed_modules and fullname not in self.allowed_modules:
            raise ImportError(f"VATA_CRITICAL_FAULT: Unauthorized import plane breach attempted for module '{fullname}'")
        
        return None  # Pass through to standard loaders if validation clears

# Global registration of the interception plane
if not any(isinstance(x, VataImportInterceptor) for x in sys.meta_path):
    interceptor = VataImportInterceptor()
    sys.meta_path.insert(0, interceptor)
    sys.modules['vata_interceptor'] = interceptor
    print("[+] VATA Core: Import Interceptor actively bound to sys.meta_path.")
