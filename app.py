"""
🎮 Game Glitch Investigator - Enhanced Edition
AI-Integrated Number Guessing Game with Strategic Assistant
Features: Agentic workflow, confidence scoring, comprehensive logging, and reliability testing
"""

import random
import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score
)
from ai_assistant import AIAssistant
from game_logger import GameEvaluator, TestValidator, setup_logging

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Game Glitch Investigator - Enhanced",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

def init_session_state():
    """Initialize all session state variables."""
    if "secret" not in st.session_state:
        st.session_state.secret = None
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "status" not in st.session_state:
        st.session_state.status = "idle"
    if "history" not in st.session_state:
        st.session_state.history = []
    if "ai_assistant" not in st.session_state:
        st.session_state.ai_assistant = None
    if "evaluator" not in st.session_state:
        st.session_state.evaluator = GameEvaluator()
    if "ai_hints_used" not in st.session_state:
        st.session_state.ai_hints_used = 0
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "Player vs AI"
    if "show_ai_hint" not in st.session_state:
        st.session_state.show_ai_hint = False
    if "ai_feedback" not in st.session_state:
        st.session_state.ai_feedback = None

init_session_state()

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

st.sidebar.title("⚙️ Game Controls")

# Game Mode Selection
game_mode = st.sidebar.radio(
    "Game Mode",
    ["Player vs AI", "Classic Mode"],
    help="Player vs AI: Get strategic hints from AI assistant\nClassic Mode: Traditional gameplay"
)

if game_mode != st.session_state.game_mode:
    st.session_state.game_mode = game_mode
    st.session_state.secret = None
    st.session_state.status = "idle"

# Difficulty Selection
difficulty = st.sidebar.selectbox(
    "Difficulty Level",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

# Display game info
st.sidebar.caption(f"📊 Range: {low} to {high}")
st.sidebar.caption(f"🎯 Attempts allowed: {attempt_limit}")

# Initialize new game if needed
if st.session_state.secret is None or st.session_state.status == "idle":
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.ai_hints_used = 0
    if game_mode == "Player vs AI":
        st.session_state.ai_assistant = AIAssistant(difficulty)
    st.session_state.ai_feedback = None

# Developer Debug Info
with st.sidebar.expander("🔍 Developer Debug Info"):
    st.write("**Secret (for testing):**", st.session_state.secret)
    st.write("**Attempts made:**", st.session_state.attempts)
    st.write("**Current score:**", st.session_state.score)
    st.write("**Game status:**", st.session_state.status)
    st.write("**Guess history:**", st.session_state.history)
    st.write("**AI assistant active:**", st.session_state.ai_assistant is not None)

# ============================================================================
# MAIN TITLE AND INTRODUCTION
# ============================================================================

st.title("🎮 Game Glitch Investigator - Enhanced Edition")
st.markdown(
    "An AI-powered number guessing game with strategic assistance. "
    "Find the secret number and maximize your score!"
)

# Display current stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Score", st.session_state.score, delta=None)
with col2:
    st.metric("Attempts Used", st.session_state.attempts, f"/{attempt_limit}")
with col3:
    st.metric("Game Mode", game_mode)
with col4:
    st.metric("Difficulty", difficulty)

st.divider()

# ============================================================================
# GAME INTERFACE
# ============================================================================

if st.session_state.status == "playing":
    # Display hint about remaining attempts
    attempts_remaining = attempt_limit - st.session_state.attempts
    progress = st.session_state.attempts / attempt_limit
    
    st.info(
        f"**Guess a number between {low} and {high}** "
        f"(Attempts remaining: {attempts_remaining})"
    )
    st.progress(progress, text=f"Progress: {st.session_state.attempts}/{attempt_limit}")
    
    # Create columns for input and buttons
    col_input, col_submit = st.columns([3, 1])
    
    with col_input:
        raw_guess = st.text_input(
            "Enter your guess:",
            placeholder="Type a number...",
            key=f"guess_input_{difficulty}_{st.session_state.attempts}"
        )
    
    with col_submit:
        submit = st.button("Submit 🚀", use_container_width=True)
    
    # AI Assistant Option (visible only in Player vs AI mode)
    if game_mode == "Player vs AI" and st.session_state.ai_assistant:
        st.divider()
        
        if st.button("Get AI Hint 🤖", use_container_width=True):
            with st.spinner("AI Assistant is analyzing..."):
                analysis = st.session_state.ai_assistant.analyze_game_state(
                    low=low,
                    high=high,
                    guesses=st.session_state.history,
                    feedback=[
                        check_guess(g, st.session_state.secret)[0]
                        for g in st.session_state.history
                    ]
                )
                st.session_state.ai_feedback = analysis
                st.session_state.ai_hints_used += 1
                st.rerun()
        
        # Display AI feedback if available
        if st.session_state.ai_feedback:
            st.info(f"**💡 AI Hint:** {st.session_state.ai_feedback['hint']}")
            
            col_conf, col_range = st.columns(2)
            with col_conf:
                confidence = st.session_state.ai_feedback['confidence']
                st.progress(confidence, text=f"Confidence: {confidence:.0%}")
            
            with col_range:
                remaining_range = st.session_state.ai_feedback['remaining_range']
                st.write(f"**Possible range:** {remaining_range[0]} - {remaining_range[1]}")
            
            with st.expander("📖 AI Reasoning"):
                st.write(st.session_state.ai_feedback['reasoning'])
    
    st.divider()
    
    # Process guess submission
    if submit and raw_guess:
        ok, guess_int, err = parse_guess(raw_guess)
        
        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(f"❌ {err}")
            st.session_state.evaluator.log_error(
                "Invalid Input",
                err,
                {"raw_input": raw_guess}
            )
        else:
            st.session_state.attempts += 1
            st.session_state.history.append(guess_int)
            
            outcome, message = check_guess(guess_int, st.session_state.secret)
            
            # Display result
            st.success(message)
            
            # Update score
            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts
            )
            
            # Check win condition
            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                
                # Log successful game
                st.session_state.evaluator.log_game_result(
                    difficulty=difficulty,
                    secret=st.session_state.secret,
                    attempts=st.session_state.attempts,
                    won=True,
                    guess_history=st.session_state.history,
                    ai_hints_used=st.session_state.ai_hints_used
                )
                
                st.balloons()
                st.success(
                    f"🎉 **YOU WIN!** The secret was **{st.session_state.secret}**\n\n"
                    f"**Final Score:** {st.session_state.score}\n"
                    f"**Attempts Used:** {st.session_state.attempts}/{attempt_limit}\n"
                    f"**AI Hints Used:** {st.session_state.ai_hints_used}"
                )
                st.rerun()
            
            # Check lose condition
            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                
                # Log failed game
                st.session_state.evaluator.log_game_result(
                    difficulty=difficulty,
                    secret=st.session_state.secret,
                    attempts=st.session_state.attempts,
                    won=False,
                    guess_history=st.session_state.history,
                    ai_hints_used=st.session_state.ai_hints_used
                )
                
                st.error(
                    f"💔 **GAME OVER!** The secret was **{st.session_state.secret}**\n\n"
                    f"**Final Score:** {st.session_state.score}\n"
                    f"**Attempts Used:** {st.session_state.attempts}/{attempt_limit}\n"
                    f"**AI Hints Used:** {st.session_state.ai_hints_used}"
                )
                st.rerun()
            
            st.rerun()

# ============================================================================
# GAME OVER STATES
# ============================================================================

elif st.session_state.status == "won":
    st.success("🎉 You already won this round! Start a new game to play again.")
elif st.session_state.status == "lost":
    st.error("💔 Game over. You've used all attempts. Start a new game to try again.")

# ============================================================================
# NEW GAME BUTTON
# ============================================================================

st.divider()

if st.button("🔁 Start New Game", use_container_width=True, type="primary"):
    st.session_state.secret = None
    st.session_state.status = "idle"
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.ai_hints_used = 0
    st.session_state.ai_feedback = None
    st.rerun()

# ============================================================================
# STATISTICS AND METRICS SECTION
# ============================================================================

st.divider()
st.subheader("📈 Statistics & Performance Metrics")

# Get reliability report
metrics = st.session_state.evaluator.get_reliability_report()

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Games Played", metrics['total_games'])
with col2:
    st.metric("Games Won", metrics['games_won'])
with col3:
    st.metric("Win Rate", f"{metrics['win_rate_percent']}%")
with col4:
    st.metric("Avg Attempts", metrics['average_attempts'])

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("System Reliability", f"{metrics['system_reliability']}%")
with col6:
    st.metric("Total Errors", metrics['total_errors'])
with col7:
    st.metric("Error Rate", f"{metrics['error_rate_percent']}%")

# ============================================================================
# AI ASSISTANT PERFORMANCE (If active)
# ============================================================================

if st.session_state.ai_assistant:
    st.divider()
    st.subheader("🤖 AI Assistant Performance")
    
    ai_metrics = st.session_state.ai_assistant.get_performance_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Games Analyzed", ai_metrics['games_analyzed'])
    with col2:
        st.metric("Success Rate", f"{ai_metrics['success_rate']*100:.1f}%")
    with col3:
        st.metric("Avg Confidence", f"{ai_metrics['average_confidence']:.2f}")
    with col4:
        st.metric("AI Hints Given", ai_metrics['total_suggestions'])
    
    # AI Summary
    with st.expander("📊 AI Assistant Summary"):
        st.write(st.session_state.ai_assistant.get_conversation_summary())

# ============================================================================
# TESTING AND VALIDATION SECTION
# ============================================================================

with st.expander("🧪 Run System Tests"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Guess Validation", use_container_width=True):
            validator = TestValidator()
            validator.test_guess_validation()
            results = validator.get_test_results()
            
            if results['failed'] == 0:
                st.success(f"✅ All {results['passed']} tests passed!")
            else:
                st.warning(f"⚠️ {results['passed']} passed, {results['failed']} failed")
            
            st.json(results)
    
    with col2:
        if st.button("Test Hint Logic", use_container_width=True):
            validator = TestValidator()
            validator.test_hint_correctness()
            results = validator.get_test_results()
            
            if results['failed'] == 0:
                st.success(f"✅ All {results['passed']} tests passed!")
            else:
                st.warning(f"⚠️ {results['passed']} passed, {results['failed']} failed")
            
            st.json(results)

# ============================================================================
# EXPORT DATA
# ============================================================================

with st.expander("💾 Export Metrics"):
    if st.button("Export Game Metrics to JSON", use_container_width=True):
        filepath = st.session_state.evaluator.export_metrics()
        st.success(f"Metrics exported to: `{filepath}`")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption(
    "🎮 **Game Glitch Investigator - Enhanced Edition** | "
    "Built with Streamlit + AI-powered assistance | "
    "Features: Agentic workflow, confidence scoring, & comprehensive logging"
)
