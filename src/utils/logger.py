import os
import time
from datetime import datetime

class Logger:
    _instance = None
    
    def __new__(cls, filename=None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, filename=None):
        if not self._initialized:
            self._initialized = True
            self.logs = []
            
            # Create log directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            
            if filename is None:
                self.filename = f"logs/game_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            else:
                self.filename = f"logs/{filename}"
    
    def log(self, message):
        """
        Log a message.
        
        Args:
            message (str): The message to log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        
        # Also write to file
        with open(self.filename, "a") as f:
            f.write(log_entry + "\n")
        
        return log_entry
    
    def get_logs(self):
        """
        Get all logs.
        
        Returns:
            list: List of log entries
        """
        return self.logs
    
    def clear(self):
        """Clear all logs."""
        self.logs = []