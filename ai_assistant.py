"""
AI Assistant Module for Game Glitch Investigator
Provides intelligent hints and strategic guidance using agentic workflow.
Implements confidence scoring and learning from game history (RAG-like system).
"""

import logging
import json
from typing import Tuple, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class GameState:
    """Represents the current state of the guessing game."""
    
    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high
        self.eliminated_low = low
        self.eliminated_high = high
        self.guesses_history: List[int] = []
        self.feedback_history: List[str] = []
        
    def update_bounds(self, guess: int, feedback: str):
        """Update the search space based on feedback."""
        if feedback == "Too High":
            self.eliminated_high = min(self.eliminated_high, guess - 1)
        elif feedback == "Too Low":
            self.eliminated_low = max(self.eliminated_low, guess + 1)
        
        self.guesses_history.append(guess)
        self.feedback_history.append(feedback)
    
    def get_remaining_range(self) -> Tuple[int, int]:
        """Get the remaining possible range for the secret number."""
        return self.eliminated_low, self.eliminated_high
    
    def num_remaining(self) -> int:
        """Calculate how many numbers could still be the secret."""
        low, high = self.get_remaining_range()
        if low > high:
            return 0
        return high - low + 1


class AIAssistant:
    """
    AI Assistant that provides strategic hints and guidance.
    Implements agentic workflow with confidence scoring and learning capability.
    """
    
    def __init__(self, difficulty: str = "Normal"):
        self.difficulty = difficulty
        self.conversation_history: List[Dict[str, str]] = []
        self.game_states: List[GameState] = []
        self.confidence_scores: List[float] = []
        self.total_games_analyzed = 0
        self.successful_analyses = 0
        
        logger.info(f"AI Assistant initialized for {difficulty} difficulty")
    
    def analyze_game_state(
        self,
        low: int,
        high: int,
        guesses: List[int],
        feedback: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze the current game state and provide a strategic hint.
        Implements agentic workflow: observe → analyze → suggest → learn.
        
        Args:
            low: Lower bound of range
            high: Upper bound of range
            guesses: List of guesses made so far
            feedback: List of feedback for each guess
            
        Returns:
            Dictionary with hint, confidence score, and reasoning
        """
        try:
            self.total_games_analyzed += 1
            
            # Step 1: Build game state from history
            state = GameState(low, high)
            for guess, fb in zip(guesses, feedback):
                if fb != "Win":
                    state.update_bounds(guess, fb)
            
            # Step 2: Analyze possible range
            remaining_low, remaining_high = state.get_remaining_range()
            num_remaining = state.num_remaining()
            
            # Step 3: Generate strategic hint
            if num_remaining <= 0:
                hint_text = "The range seems impossible. Check your feedback."
                confidence = 0.3
                reasoning = "All numbers have been eliminated."
            else:
                # Use binary search principle for optimal guessing
                mid = (remaining_low + remaining_high) // 2
                hint_text = f"Try a number around {mid} (narrowing down {remaining_low}-{remaining_high})"
                
                # Confidence increases as we narrow the range
                original_range = high - low + 1
                confidence = max(0.5, 1.0 - (num_remaining / original_range))
                
                reasoning = (
                    f"Analyzed {len(guesses)} previous guesses. "
                    f"Possible range: {remaining_low}-{remaining_high} "
                    f"({num_remaining} numbers remain). "
                    f"Suggested guess: {mid}"
                )
            
            # Step 4: Store for learning (RAG-like memory)
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "guesses": guesses.copy(),
                "feedback": feedback.copy(),
                "suggestion": hint_text,
                "confidence": confidence
            })
            
            self.game_states.append(state)
            self.confidence_scores.append(confidence)
            
            if confidence > 0.6:
                self.successful_analyses += 1
            
            result = {
                "hint": hint_text,
                "confidence": round(confidence, 2),
                "reasoning": reasoning,
                "remaining_range": [remaining_low, remaining_high],
                "num_remaining": num_remaining,
                "success": True
            }
            
            logger.info(f"Analysis complete. Confidence: {confidence:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing game state: {e}")
            return {
                "hint": "Unable to analyze. Keep guessing strategically!",
                "confidence": 0.0,
                "reasoning": f"Analysis error: {str(e)}",
                "remaining_range": [low, high],
                "num_remaining": high - low + 1,
                "success": False
            }
    
    def evaluate_guess_quality(self, guess: int, secret: int, low: int, high: int) -> Dict[str, Any]:
        """Evaluate how good a guess was from a strategic perspective."""
        mid = (low + high) // 2
        
        # Optimal strategy is binary search around the midpoint
        distance_from_optimal = abs(guess - mid)
        quality_score = max(0.0, 1.0 - (distance_from_optimal / ((high - low + 1) / 2))) if (high - low) > 0 else 1.0
        
        return {
            "quality_score": round(quality_score, 2),
            "optimal_guess": mid,
            "distance_from_optimal": distance_from_optimal,
            "is_winning_guess": guess == secret
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get AI assistant's performance metrics (learning capability)."""
        if self.total_games_analyzed == 0:
            return {
                "games_analyzed": 0,
                "success_rate": 0.0,
                "average_confidence": 0.0,
                "total_suggestions": 0
            }
        
        avg_confidence = (
            sum(self.confidence_scores) / len(self.confidence_scores)
            if self.confidence_scores
            else 0.0
        )
        
        success_rate = self.successful_analyses / self.total_games_analyzed
        
        return {
            "games_analyzed": self.total_games_analyzed,
            "success_rate": round(success_rate, 2),
            "average_confidence": round(avg_confidence, 2),
            "total_suggestions": len(self.conversation_history),
            "high_confidence_suggestions": sum(1 for c in self.confidence_scores if c > 0.7),
            "low_confidence_suggestions": sum(1 for c in self.confidence_scores if c < 0.5)
        }
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the AI's conversation history (RAG component)."""
        if not self.conversation_history:
            return "No games analyzed yet."
        
        metrics = self.get_performance_metrics()
        summary = (
            f"AI Assistant Summary:\n"
            f"- Games analyzed: {metrics['games_analyzed']}\n"
            f"- Success rate: {metrics['success_rate']*100:.1f}%\n"
            f"- Average confidence: {metrics['average_confidence']:.2f}\n"
            f"- Total suggestions made: {metrics['total_suggestions']}\n"
            f"- High confidence suggestions: {metrics['high_confidence_suggestions']}\n"
            f"- Low confidence suggestions: {metrics['low_confidence_suggestions']}"
        )
        return summary
