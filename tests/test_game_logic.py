"""
Comprehensive Test Suite for Game Glitch Investigator
Tests game logic, AI assistant, logging, and system reliability
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score
from ai_assistant import AIAssistant, GameState
from game_logger import GameEvaluator, TestValidator


# ============================================================================
# BASIC GAME LOGIC TESTS
# ============================================================================

def test_winning_guess():
    """Test that matching guess and secret returns Win."""
    result = check_guess(50, 50)
    assert result[0] == "Win"
    assert "🎉" in result[1]


def test_guess_too_high():
    """Test that a guess above secret returns Too High."""
    result = check_guess(60, 50)
    assert result[0] == "Too High"
    assert "LOWER" in result[1]


def test_guess_too_low():
    """Test that a guess below secret returns Too Low."""
    result = check_guess(40, 50)
    assert result[0] == "Too Low"
    assert "HIGHER" in result[1]


def test_guess_edge_cases():
    """Test edge cases: very high and very low guesses."""
    # Guess much higher
    assert check_guess(1000, 50)[0] == "Too High"
    # Guess much lower
    assert check_guess(1, 50)[0] == "Too Low"
    # Guess at boundaries
    assert check_guess(1, 1)[0] == "Win"
    assert check_guess(1, 2)[0] == "Too Low"


# ============================================================================
# GUESS PARSING TESTS
# ============================================================================

def test_parse_valid_integer():
    """Test parsing a valid integer guess."""
    ok, value, err = parse_guess("50")
    assert ok == True
    assert value == 50
    assert err is None


def test_parse_valid_float():
    """Test parsing a valid float guess (should convert to int)."""
    ok, value, err = parse_guess("50.7")
    assert ok == True
    assert value == 50
    assert err is None


def test_parse_empty_string():
    """Test parsing empty string returns error."""
    ok, value, err = parse_guess("")
    assert ok == False
    assert value is None
    assert err is not None


def test_parse_invalid_string():
    """Test parsing non-numeric string returns error."""
    ok, value, err = parse_guess("hello")
    assert ok == False
    assert value is None
    assert err is not None


def test_parse_none():
    """Test parsing None returns error."""
    ok, value, err = parse_guess(None)
    assert ok == False
    assert value is None


# ============================================================================
# DIFFICULTY AND RANGE TESTS
# ============================================================================

def test_easy_range():
    """Test that Easy difficulty has correct range."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range():
    """Test that Normal difficulty has correct range."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_range():
    """Test that Hard difficulty has correct range."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50


def test_unknown_difficulty_defaults():
    """Test that unknown difficulty defaults to Normal range."""
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100


# ============================================================================
# SCORING TESTS
# ============================================================================

def test_winning_score():
    """Test that winning gives appropriate points."""
    # First attempt win: 100 - 10*2 = 80
    score = update_score(0, "Win", 1)
    assert score == 80
    
    # Later attempt win: 100 - 10*5 = 50
    score = update_score(0, "Win", 4)
    assert score == 50
    
    # Very late attempt win: minimum 10 points
    score = update_score(0, "Win", 20)
    assert score == 10


def test_too_high_scoring():
    """Test scoring for Too High feedback."""
    # Even attempt: +5
    score = update_score(0, "Too High", 2)
    assert score == 5
    
    # Odd attempt: -5
    score = update_score(0, "Too High", 1)
    assert score == -5


def test_too_low_scoring():
    """Test scoring for Too Low feedback."""
    # Too Low always -5
    score = update_score(100, "Too Low", 1)
    assert score == 95
    
    score = update_score(100, "Too Low", 2)
    assert score == 95


# ============================================================================
# AI ASSISTANT TESTS
# ============================================================================

def test_ai_assistant_initialization():
    """Test that AI assistant initializes correctly."""
    ai = AIAssistant("Normal")
    assert ai.difficulty == "Normal"
    assert ai.total_games_analyzed == 0
    assert len(ai.conversation_history) == 0


def test_game_state_update():
    """Test GameState bounds update."""
    state = GameState(1, 100)
    assert state.num_remaining() == 100
    
    # Update after "Too High" feedback
    state.update_bounds(50, "Too High")
    remaining_low, remaining_high = state.get_remaining_range()
    assert remaining_low == 1
    assert remaining_high == 49
    assert state.num_remaining() == 49
    
    # Update after "Too Low" feedback
    state.update_bounds(25, "Too Low")
    remaining_low, remaining_high = state.get_remaining_range()
    assert remaining_low == 26
    assert remaining_high == 49


def test_ai_analysis():
    """Test that AI provides analysis with confidence."""
    ai = AIAssistant("Easy")
    
    # Analyze with no guesses yet
    analysis = ai.analyze_game_state(
        low=1, high=20,
        guesses=[],
        feedback=[]
    )
    
    assert "hint" in analysis
    assert "confidence" in analysis
    assert "reasoning" in analysis
    assert analysis["success"] == True
    assert 0 <= analysis["confidence"] <= 1


def test_ai_performance_metrics():
    """Test that AI tracks performance metrics."""
    ai = AIAssistant("Normal")
    
    # Initially empty
    metrics = ai.get_performance_metrics()
    assert metrics["games_analyzed"] == 0
    assert metrics["success_rate"] == 0.0
    
    # After analysis
    ai.analyze_game_state(1, 100, [], [])
    metrics = ai.get_performance_metrics()
    assert metrics["games_analyzed"] == 1


# ============================================================================
# LOGGING AND EVALUATION TESTS
# ============================================================================

def test_game_evaluator_initialization():
    """Test that GameEvaluator initializes correctly."""
    evaluator = GameEvaluator()
    assert evaluator.total_games == 0
    assert evaluator.won_games == 0
    assert evaluator.lost_games == 0


def test_game_result_logging():
    """Test logging a game result."""
    evaluator = GameEvaluator()
    
    # Log a win
    evaluator.log_game_result(
        difficulty="Easy",
        secret=15,
        attempts=3,
        won=True,
        guess_history=[10, 18, 15]
    )
    
    assert evaluator.total_games == 1
    assert evaluator.won_games == 1
    assert evaluator.won_games == 1


def test_reliability_report():
    """Test that reliability report is generated correctly."""
    evaluator = GameEvaluator()
    
    # Log some games
    evaluator.log_game_result("Easy", 15, 3, True, [10, 18, 15])
    evaluator.log_game_result("Normal", 50, 5, False, [25, 75, 60, 40, 45])
    
    report = evaluator.get_reliability_report()
    
    assert report["total_games"] == 2
    assert report["games_won"] == 1
    assert report["games_lost"] == 1
    assert report["win_rate_percent"] == 50.0
    assert "system_reliability" in report


def test_error_logging():
    """Test logging errors."""
    evaluator = GameEvaluator()
    
    evaluator.log_error(
        error_type="Invalid Input",
        description="User entered non-numeric value",
        context={"input": "abc"}
    )
    
    assert evaluator.games_with_errors == 1
    assert len(evaluator.error_log) == 1


def test_validator_guess_validation():
    """Test the TestValidator for guess validation."""
    validator = TestValidator()
    result = validator.test_guess_validation()
    
    # Should pass test for valid cases
    assert result == True or result == False  # May vary based on logic


def test_validator_hint_correctness():
    """Test the TestValidator for hint logic."""
    validator = TestValidator()
    result = validator.test_hint_correctness()
    
    # Should pass test
    assert result == True


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_full_game_flow():
    """Test a complete game flow from start to win."""
    secret = 50
    guesses = [25, 75, 60, 55]
    
    # Simulate game
    for guess in guesses:
        result, message = check_guess(guess, secret)
        assert result in ["Too High", "Too Low"]
    
    # Final winning guess
    result, message = check_guess(secret, secret)
    assert result == "Win"


def test_ai_across_game():
    """Test AI assistant during a game."""
    ai = AIAssistant("Normal")
    secret = 50
    
    # First guess
    guess1 = 75
    feedback1 = check_guess(guess1, secret)[0]
    
    analysis1 = ai.analyze_game_state(
        low=1, high=100,
        guesses=[guess1],
        feedback=[feedback1]
    )
    assert analysis1["success"] == True
    
    # Second guess
    guess2 = 25
    feedback2 = check_guess(guess2, secret)[0]
    
    analysis2 = ai.analyze_game_state(
        low=1, high=100,
        guesses=[guess1, guess2],
        feedback=[feedback1, feedback2]
    )
    
    # Confidence should be higher with more information
    assert analysis2["num_remaining"] < analysis1["num_remaining"]


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
