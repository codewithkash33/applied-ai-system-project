"""
Game Logger and Evaluation System
Provides comprehensive logging, metrics tracking, and reliability evaluation.
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys

# Configure logging
def setup_logging(log_file: str = "game_logs.txt"):
    """Set up comprehensive logging for the game."""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_path = log_dir / log_file
    
    # Create logger
    logger = logging.getLogger("game_logger")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


class GameEvaluator:
    """
    Evaluates game performance and reliability.
    Tracks metrics for assessing system robustness.
    """
    
    def __init__(self):
        self.total_games = 0
        self.won_games = 0
        self.lost_games = 0
        self.games_with_errors = 0
        self.average_attempts = 0
        self.all_attempt_counts = []
        self.ai_hint_accuracy = []
        self.user_satisfaction_scores = []
        self.error_log = []
        
        self.logger = setup_logging()
        self.logger.info("GameEvaluator initialized")
    
    def log_game_result(
        self,
        difficulty: str,
        secret: int,
        attempts: int,
        won: bool,
        guess_history: List[int],
        ai_hints_used: int = 0
    ):
        """Log a completed game and its statistics."""
        self.total_games += 1
        
        if won:
            self.won_games += 1
        else:
            self.lost_games += 1
        
        self.all_attempt_counts.append(attempts)
        self.average_attempts = sum(self.all_attempt_counts) / len(self.all_attempt_counts)
        
        win_rate = (self.won_games / self.total_games) * 100 if self.total_games > 0 else 0
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "difficulty": difficulty,
            "secret_number": secret,
            "attempts": attempts,
            "won": won,
            "guess_history": guess_history,
            "ai_hints_used": ai_hints_used,
            "total_games_played": self.total_games,
            "current_win_rate": round(win_rate, 1)
        }
        
        self.logger.info(
            f"Game #{self.total_games} completed | "
            f"Difficulty: {difficulty} | "
            f"Result: {'WON' if won else 'LOST'} | "
            f"Attempts: {attempts} | "
            f"Win Rate: {win_rate:.1f}%"
        )
        
        return log_entry
    
    def log_error(self, error_type: str, description: str, context: Dict[str, Any] = None):
        """Log an error or issue encountered during gameplay."""
        self.games_with_errors += 1
        
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "description": description,
            "context": context or {}
        }
        
        self.error_log.append(error_entry)
        self.logger.error(f"[{error_type}] {description}")
        
        return error_entry
    
    def log_ai_hint(
        self,
        hint_text: str,
        confidence: float,
        was_helpful: bool = None
    ):
        """Log an AI hint and whether it was helpful."""
        hint_entry = {
            "timestamp": datetime.now().isoformat(),
            "hint": hint_text,
            "confidence": confidence,
            "was_helpful": was_helpful
        }
        
        if was_helpful is not None:
            self.ai_hint_accuracy.append(1.0 if was_helpful else 0.0)
        
        self.logger.info(f"AI Hint | Confidence: {confidence:.2f} | Helpful: {was_helpful}")
        
        return hint_entry
    
    def get_reliability_report(self) -> Dict[str, Any]:
        """Generate a comprehensive reliability report."""
        win_rate = (self.won_games / self.total_games * 100) if self.total_games > 0 else 0
        error_rate = (self.games_with_errors / self.total_games * 100) if self.total_games > 0 else 0
        avg_hint_accuracy = (
            sum(self.ai_hint_accuracy) / len(self.ai_hint_accuracy) * 100
            if self.ai_hint_accuracy
            else 0
        )
        
        report = {
            "total_games": self.total_games,
            "games_won": self.won_games,
            "games_lost": self.lost_games,
            "win_rate_percent": round(win_rate, 1),
            "error_rate_percent": round(error_rate, 1),
            "average_attempts": round(self.average_attempts, 1),
            "ai_hint_accuracy_percent": round(avg_hint_accuracy, 1),
            "total_errors": len(self.error_log),
            "system_reliability": round(100 - error_rate, 1),
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"Reliability Report Generated: {json.dumps(report, indent=2)}")
        
        return report
    
    def export_metrics(self, filename: str = "game_metrics.json"):
        """Export all collected metrics to a JSON file."""
        metrics = {
            "summary": self.get_reliability_report(),
            "error_log": self.error_log
        }
        
        metrics_dir = Path(__file__).parent / "metrics"
        metrics_dir.mkdir(exist_ok=True)
        
        filepath = metrics_dir / filename
        with open(filepath, "w") as f:
            json.dump(metrics, f, indent=2)
        
        self.logger.info(f"Metrics exported to {filepath}")
        return filepath
    
    def reset(self):
        """Reset all metrics (for testing purposes)."""
        self.__init__()
        self.logger.info("Metrics reset")


class TestValidator:
    """Validates that the game behaves reliably."""
    
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        self.logger = logging.getLogger("game_logger")
    
    def test_guess_validation(self) -> bool:
        """Test that invalid guesses are properly rejected."""
        from logic_utils import parse_guess
        
        test_cases = [
            ("50", True),
            ("not_a_number", False),
            ("", False),
            ("50.5", True),
            (None, False),
        ]
        
        for raw_input, should_be_valid in test_cases:
            ok, _, _ = parse_guess(raw_input) if raw_input is not None else parse_guess("")
            if ok == should_be_valid:
                self.passed_tests += 1
                self.logger.info(f"✓ Guess validation test passed: {raw_input}")
            else:
                self.failed_tests += 1
                self.logger.error(f"✗ Guess validation test failed: {raw_input}")
        
        return self.failed_tests == 0
    
    def test_hint_correctness(self) -> bool:
        """Test that hints are correct."""
        from logic_utils import check_guess
        
        test_cases = [
            (50, 50, "Win"),
            (60, 50, "Too High"),
            (40, 50, "Too Low"),
            (1, 100, "Too Low"),
            (100, 99, "Too High"),
        ]
        
        for guess, secret, expected_outcome in test_cases:
            outcome, _ = check_guess(guess, secret)
            if outcome == expected_outcome:
                self.passed_tests += 1
                self.logger.info(f"✓ Hint test passed: guess={guess}, secret={secret}")
            else:
                self.failed_tests += 1
                self.logger.error(
                    f"✗ Hint test failed: guess={guess}, secret={secret}, "
                    f"expected={expected_outcome}, got={outcome}"
                )
        
        return self.failed_tests == 0
    
    def get_test_results(self) -> Dict[str, Any]:
        """Get test results summary."""
        total = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total * 100) if total > 0 else 0
        
        return {
            "total_tests": total,
            "passed": self.passed_tests,
            "failed": self.failed_tests,
            "pass_rate_percent": round(pass_rate, 1)
        }
