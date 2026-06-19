import os
import sys
import psutil

class ResourceMonitor:
    # Initialize a class variable to track the last CPU check time.
    # This avoids blocking calls while maintaining cross-OS precision.
    _initialized = False

    @classmethod
    def _ensure_ready(cls):
        """Pre-warms the CPU timer so the first measurement isn't broken or blocking."""
        if not cls._initialized:
            psutil.cpu_percent(interval=None)
            cls._initialized = True

    @classmethod
    def get_system_stats(cls):
        """
        Captures CPU and RAM metrics across Windows, macOS, and Linux.
        Uses non-blocking interval=None to ensure compatibility with multi-threaded runtimes.
        """
        cls._ensure_ready()
        
        try:
            # interval=None reads system CPU cycles immediately without blocking the current thread
            cpu_usage = psutil.cpu_percent(interval=None)
            memory_info = psutil.virtual_memory()
            
            # Fallback handling: If the very first call returns 0.0 due to OS timing constraints
            if cpu_usage == 0.0:
                # Provide a fallback method using the current process status if system wider metrics are delayed
                cpu_usage = round(psutil.Process(os.getpid()).cpu_percent(interval=None), 2)
            
            return {
                "cpu_percent": min(max(cpu_usage, 0.0), 100.0), # Boundaries to keep metrics between 0-100%
                "memory_percent": round(memory_info.percent, 2),
                "os_platform": sys.platform
            }
            
        except Exception:
            # Safe absolute fallback defaults if an OS limits permission access to system telemetry
            return {
                "cpu_percent": 0.0,
                "memory_percent": 0.0,
                "os_platform": sys.platform
            }