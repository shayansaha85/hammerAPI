import concurrent.futures
import time
import httpx
from .monitor import ResourceMonitor
from .reporter import ReportGenerator

class HammerAPI:
    def __init__(self, max_workers=4):
        """Initialise HammerAPI with a designated thread worker count."""
        self.max_workers = max_workers
        self.test_cases = []
        self.results = []
        self.total_duration = 0  # Tracked for reporting

    def add_test(self, method, url, **kwargs):
        """Queue up a configuration setup for an API endpoint test."""
        self.test_cases.append({
            "method": method.upper(), 
            "url": url, 
            "options": kwargs
        })

    def _execute_single(self, test):
        """Worker executing dynamic HTTP clients concurrently alongside system monitoring."""
        start_resources = ResourceMonitor.get_system_stats()
        start_time = time.perf_counter()
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.request(test["method"], test["url"], **test["options"])
                status = response.status_code
        except Exception as e:
            status = f"Network Error: {str(e)}"

        latency = time.perf_counter() - start_time
        end_resources = ResourceMonitor.get_system_stats()

        return {
            "method": test["method"],
            "url": test["url"],
            "status": status,
            "latency_ms": round(latency * 1000, 2),
            "cpu_usage_avg": round((start_resources["cpu_percent"] + end_resources["cpu_percent"]) / 2, 2),
            "ram_usage_avg": round((start_resources["memory_percent"] + end_resources["memory_percent"]) / 2, 2),
            "timestamp": time.time()  # Track when it happened for reporting
        }

    def run(self, duration_seconds=None):
        """
        Spawns the bounded thread pool to crush the queued API operations.
        If duration_seconds is provided, it will continuously hit the APIs for that amount of time.
        """
        if not self.test_cases:
            print("⚠️ No test cases defined. Use .add_test() first.")
            return []

        self.results = []
        start_suite_time = time.perf_counter()

        # Mode 1: Duration-based testing (Keep hitting for X seconds)
        if duration_seconds:
            print(f"🔨 [HammerAPI] Unleashing tests across {self.max_workers} threads for {duration_seconds} seconds...")
            
            end_time = start_suite_time + duration_seconds
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = set()
                test_index = 0
                
                # Keep looping until the duration expires
                while time.perf_counter() < end_time:
                    # Top up the thread pool if it has room
                    while len(futures) < self.max_workers and time.perf_counter() < end_time:
                        # Cycle through user's defined tests indefinitely
                        current_test = self.test_cases[test_index % len(self.test_cases)]
                        futures.add(executor.submit(self._execute_single, current_test))
                        test_index += 1
                    
                    # Wait for at least one thread to finish before adding more to prevent memory flooding
                    completed, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                    for future in completed:
                        self.results.append(future.result())
                
                # Clean up any leftover active threads after time expires
                if futures:
                    for future in concurrent.futures.as_completed(futures):
                        self.results.append(future.result())

            self.total_duration = round(time.perf_counter() - start_suite_time, 2)

        # Mode 2: Standard execution (Hit each queued test exactly once)
        else:
            print(f"🔨 [HammerAPI] Unleashing {len(self.test_cases)} tests across {self.max_workers} threads once...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # To make it a bit heavier, we execute the exact batch once
                self.results = list(executor.map(self._execute_single, self.test_cases))
            self.total_duration = round(time.perf_counter() - start_suite_time, 2)
            
        print(f"✅ [HammerAPI] Workload processing completed. Executed {len(self.results)} total requests.")
        return self.results

    def generate_report(self, output_path="hammer_report.html"):
        """Compiles tracked metrics arrays to the disk as HTML layout."""
        ReportGenerator.generate(self.results, self.total_duration, self.max_workers, output_path)