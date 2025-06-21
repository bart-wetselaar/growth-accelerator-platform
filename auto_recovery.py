"""
Auto-Recovery System for Growth Accelerator Platform
Automatic error detection and system restoration
"""
import logging
import time
import threading
from datetime import datetime
from error_handler import error_handler
from self_diagnostic import diagnostic_system

class AutoRecoverySystem:
    def __init__(self):
        self.logger = logging.getLogger('GA_AutoRecovery')
        self.recovery_active = True
        self.recovery_thread = None
        self.last_recovery = None
        self.recovery_count = 0
        
    def start_monitoring(self):
        """Start continuous monitoring and auto-recovery"""
        if self.recovery_thread and self.recovery_thread.is_alive():
            self.logger.warning("Auto-recovery already running")
            return
        
        self.recovery_active = True
        self.recovery_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.recovery_thread.start()
        self.logger.info("Auto-recovery system started")
    
    def stop_monitoring(self):
        """Stop auto-recovery monitoring"""
        self.recovery_active = False
        self.logger.info("Auto-recovery system stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.recovery_active:
            try:
                # Run health check every 60 seconds
                health_report = error_handler.health_check()
                
                if health_report.get('overall_status') != 'healthy':
                    self.logger.warning("Unhealthy system detected, initiating recovery")
                    self._initiate_recovery()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(30)  # Shorter interval on error
    
    def _initiate_recovery(self):
        """Initiate automatic system recovery"""
        try:
            self.logger.info("Starting automatic system recovery")
            self.recovery_count += 1
            self.last_recovery = datetime.now()
            
            # Run comprehensive diagnostics
            diagnostics = diagnostic_system.run_comprehensive_diagnostics()
            
            # Apply automatic fixes based on findings
            fixes_applied = []
            
            for component, result in diagnostics.get('components', {}).items():
                if not result.get('status', True):
                    fix_method = getattr(diagnostic_system, f'fix_{component}', None)
                    if fix_method:
                        try:
                            if fix_method():
                                fixes_applied.append(component)
                                self.logger.info(f"Auto-fix applied for {component}")
                        except Exception as fix_error:
                            self.logger.error(f"Auto-fix failed for {component}: {fix_error}")
            
            # Log recovery results
            if fixes_applied:
                self.logger.info(f"Recovery completed. Fixed components: {fixes_applied}")
            else:
                self.logger.warning("Recovery attempted but no fixes were applied")
            
            return fixes_applied
            
        except Exception as e:
            self.logger.error(f"Recovery process failed: {e}")
            return []
    
    def get_recovery_status(self):
        """Get current recovery system status"""
        return {
            'active': self.recovery_active,
            'last_recovery': self.last_recovery.isoformat() if self.last_recovery else None,
            'recovery_count': self.recovery_count,
            'monitoring': self.recovery_thread.is_alive() if self.recovery_thread else False
        }

# Global auto-recovery instance
auto_recovery = AutoRecoverySystem()