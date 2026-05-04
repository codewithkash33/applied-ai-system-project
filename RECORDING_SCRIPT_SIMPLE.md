# 📝 SIMPLE RECORDING SCRIPT - PRINT THIS
## Easy-to-Read Version for While You Record

---

## [0:00-0:30] INTRODUCTION

```
Hello! I'm demonstrating the Game Glitch Investigator - Enhanced Edition, 
an AI-powered number guessing game that evolved from a simple debugging 
exercise into a sophisticated system with intelligent AI assistance.

In this walkthrough, I'll show you:
✓ The game working in two modes
✓ The AI's agentic workflow with confidence scoring
✓ The system's reliability guardrails
✓ Real-time metrics and validation

Let's get started!
```

---

## [0:30-2:00] CLASSIC MODE - 4 GUESSES

### When starting:
```
I'll select Easy difficulty, so I'm guessing between 1 and 20 
with 6 attempts max.
```

### After GUESS 1:
```
The game tells me to go [HIGHER/LOWER]. 
Notice the attempt counter updated to 1 out of 6.
```

### After GUESS 2:
```
Trying the next number. It says go [HIGHER/LOWER]. 
The secret number is getting narrower.
```

### After GUESS 3:
```
Another guess, continuing to narrow down the range.
```

### After GUESS 4 (WINNING):
```
And we got it! The game shows we won in [X] attempts 
with a score of [read the score].

Notice the statistics at the bottom showing our win rate 
and performance metrics. This is the basic gameplay - immediate 
feedback, clear scoring, and real-time updates.
```

---

## [2:00-4:00] PLAYER VS AI MODE - MOST IMPORTANT

### When switching modes:
```
Now let's see the main feature - the AI Assistant with its 
intelligent workflow. I'm switching to Player vs AI mode.

I'm selecting Player vs AI with Normal difficulty. 
This is where the system demonstrates its agentic behavior - 
the AI observes, analyzes, and makes suggestions based on 
game state.
```

### After GUESS 1 (Type "50"):
```
I'll start with 50. The game gives me feedback: go [HIGHER/LOWER].
```

### WHEN REQUESTING AI HINT:
```
Now watch this - I'm clicking the 'Get AI Hint' button. 
The AI is going to analyze the game state and provide a strategic 
suggestion with a confidence score.
```

### WHEN HINT APPEARS:
```
Look at what the AI provided:
- Suggestion: [read the number it suggests]
- Confidence score: [read it, example: 0.75]
- Reasoning: [read the explanation provided]

Notice the confidence is NOT 100% - the AI is transparent about 
uncertainty. This is a guardrail against false confidence.
```

### After GUESS 2 (following AI):
```
I'll follow the AI's suggestion. [Type the number shown].

Good - the AI was right! This narrows our search space further.
```

### WHEN REQUESTING SECOND HINT:
```
Let's ask for another hint. Now the AI has MORE information - 
it's learned from our game history. Watch how the confidence 
changes.

The new confidence is: [read the new number - should be higher]

This demonstrates the RAG (Retrieval-Augmented Generation) pattern - 
the AI learning from history makes better suggestions.
```

### After FINAL GUESS (WINNING):
```
One final guess... [number]... and we've won!

See how we finished in fewer attempts because of the AI's guidance. 
The confidence scores were accurate, and the system showed clear 
reasoning with each hint.
```

---

## [4:00-5:00] TESTING & VALIDATION

### When showing tests:
```
Now let's look at the reliability features - automated guardrails 
that keep this system safe and consistent.
```

### After clicking "Test Guess Validation":
```
The system is testing several scenarios: valid integers, valid floats, 
empty input, invalid text. The guardrails check that all edge cases 
are handled correctly.

All tests passed! This shows the guardrails are working - invalid 
inputs are rejected, valid ones are parsed correctly, and edge cases 
don't crash the system.
```

### After clicking "Test Hint Logic":
```
One more test - checking that hint logic is always correct. 
Win, Too High, Too Low - all tested.

Perfect - 100% pass rate. These automated tests catch bugs 
before users see them.
```

---

## [5:00-6:00] METRICS & DASHBOARD

### When showing statistics:
```
Finally, the metrics and observability features. The system 
tracks detailed statistics about gameplay and AI performance.

After our games, the system shows comprehensive metrics:
- Win rate
- Average attempts
- System reliability

This helps understand how the system is performing overall.

The system also tracks AI performance separately - this is 
important for transparency about how the AI is doing.
```

### If showing export:
```
The system can export all metrics to JSON for further analysis. 
This creates a complete audit trail of everything the system did.
```

---

## [6:00-6:30] CONCLUSION

```
That's the Game Glitch Investigator - Enhanced Edition in action.

What we demonstrated:
✅ End-to-end gameplay with immediate feedback
✅ Agentic AI with confidence scoring and learning
✅ Automatic validation and testing
✅ Real-time metrics and observability

This system started as a simple debugging exercise and evolved 
into a production-ready AI application. 

All code, documentation, and ethical analysis are in the repository.

Thanks for watching!
```

---

---

## 🎬 TIMING REFERENCE

```
Total: 6-7 minutes

[0:00-0:30] = 30 sec   - Introduction
[0:30-2:00] = 90 sec   - Classic Mode (4 guesses)
[2:00-4:00] = 120 sec  - AI Mode (2-3 guesses + 2 hints)
[4:00-5:00] = 60 sec   - Testing section
[5:00-6:00] = 60 sec   - Metrics dashboard
[6:00-6:30] = 30 sec   - Conclusion
```

---

## 💡 DELIVERY TIPS

✅ **Speak naturally** - don't read like a robot
✅ **Pause after key points** - let viewers absorb
✅ **Point at screen** - helps viewers follow along
✅ **Slow down clicks** - people need time to see what you're clicking
✅ **Show numbers clearly** - confidence scores, attempt counts
✅ **Let hints load** - don't rush while AI is processing
✅ **Emphasize the word "AI"** - that's the key differentiator
✅ **Show that it works** - confidence increases, suggestions are right
✅ **End confident** - you just showed something impressive!

---

## 🆘 IF YOU MESS UP

✅ **Don't stop recording** - keep going!
✅ **Small mistakes okay** - viewers won't notice
✅ **If major issue** - You can edit in Loom or just restart

---

Print this page or put it on a second monitor while recording!
