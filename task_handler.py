import lvgl as lv
import micropython
import sys

try:
    from machine import Timer
except:
    Timer = None

class TaskHandler:
    """
    Simple LVGL task handler for ESP32-S3
    Manages the LVGL timer and task handler loop
    """
    def __init__(self, freq=25, timer_id=-1):
        """
        Initialize the task handler
        
        Args:
            freq: Refresh frequency in Hz (default 25Hz = 40ms period)
            timer_id: Timer ID to use (-1 for software timer on ESP32)
        """
        if not lv.is_initialized():
            lv.init()
        
        self.delay = 1000 // freq  # Convert Hz to ms
        self.scheduled = 0
        self.max_scheduled = 2
        
        # Create timer for periodic LVGL updates
        if Timer:
            self.timer = Timer(timer_id)
            self.timer.init(
                mode=Timer.PERIODIC,
                period=self.delay,
                callback=self._timer_callback
            )
            self.task_handler_ref = self._task_handler
        else:
            raise RuntimeError("Timer not available on this platform")
    
    def _timer_callback(self, timer):
        """Called by hardware timer - runs in interrupt context"""
        lv.tick_inc(self.delay)
        if self.scheduled < self.max_scheduled:
            try:
                micropython.schedule(self.task_handler_ref, 0)
                self.scheduled += 1
            except:
                pass
    
    def _task_handler(self, _):
        """Scheduled task handler - runs in main thread context"""
        try:
            lv.task_handler()
            self.scheduled -= 1
        except Exception as e:
            sys.print_exception(e)
    
    def deinit(self):
        """Stop the task handler and clean up"""
        if hasattr(self, 'timer') and self.timer:
            self.timer.deinit()
