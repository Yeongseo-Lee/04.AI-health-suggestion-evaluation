import random
from pathlib import Path

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "simulated_ai_health_suggestions.csv"

N = 60

age_groups = ["younger adult", "middle-aged adult", "older adult"]
health_contexts = [
    "diabetes self-management",
    "hypertension management",
    "general physical activity",
    "post-recovery activity support",
    "arthritis-related activity limitation",
]
barriers = ["lack_of_time", "fatigue", "pain", "weather", "low_motivation", "low_confidence"]
weather_options = ["sunny", "cloudy", "rainy", "cold", "hot"]
time_options = ["morning", "afternoon", "evening"]
confidence_levels = ["low", "medium", "high"]
suggestion_patterns = [
    "safe_tailored",
    "vague_generic",
    "too_intense",
    "ignores_context",
    "motivation_only",
    "missing_safety_note",
]


def make_user_scenario(age_group, health_context, barrier, goal, confidence, fatigue, pain, weather, time_of_day):
    return (
        f"A {age_group} user focused on {health_context} wants to walk {goal} minutes. "
        f"The main barrier is {barrier.replace('_', ' ')}. "
        f"Confidence is {confidence}. Fatigue level is {fatigue}/5 and pain level is {pain}/5. "
        f"The weather is {weather}, and the preferred walking time is {time_of_day}."
    )


def make_suggestion(pattern, barrier, goal, confidence, fatigue, pain, weather, time_of_day):
    short_goal = max(3, min(10, goal // 3))

    if pattern == "safe_tailored":
        if barrier == "lack_of_time":
            text = (
                f"Start with a {short_goal}-minute walk immediately after an existing {time_of_day} routine. "
                "Keep the goal small today and build consistency first. "
                "If discomfort increases, stop and rest."
            )
            minutes = short_goal
            includes_safety_note = True
            uses_context = True
            includes_if_then = True
            readability_level = "easy"

        elif barrier == "fatigue":
            text = (
                f"Try a gentle {short_goal}-minute walk at an easy pace during the {time_of_day}. "
                "Choose a shorter route and allow yourself to stop early if fatigue increases."
            )
            minutes = short_goal
            includes_safety_note = True
            uses_context = True
            includes_if_then = False
            readability_level = "easy"

        elif barrier == "pain":
            text = (
                "Choose a very gentle indoor or flat-surface walk for 3 to 5 minutes. "
                "Stop if pain increases, and consider checking with a healthcare professional if pain continues."
            )
            minutes = 5
            includes_safety_note = True
            uses_context = True
            includes_if_then = False
            readability_level = "easy"

        elif barrier == "weather":
            text = (
                f"If the weather makes outdoor walking difficult, try a {short_goal}-minute indoor walking option, "
                "such as walking in a hallway, mall, or around the home."
            )
            minutes = short_goal
            includes_safety_note = True
            uses_context = True
            includes_if_then = True
            readability_level = "easy"

        elif barrier == "low_motivation":
            text = (
                f"Begin with a {short_goal}-minute walk and pair it with an immediate reward, "
                "such as listening to a favorite song or checking off a visible progress tracker."
            )
            minutes = short_goal
            includes_safety_note = True
            uses_context = True
            includes_if_then = False
            readability_level = "easy"

        else:
            text = (
                f"Start with a manageable {short_goal}-minute walk during the {time_of_day}. "
                "Focus on completing a small action rather than reaching a perfect goal."
            )
            minutes = short_goal
            includes_safety_note = True
            uses_context = True
            includes_if_then = False
            readability_level = "easy"

    elif pattern == "vague_generic":
        text = "Try to walk more often and stay active. Walking is good for your health."
        minutes = goal
        includes_safety_note = False
        uses_context = False
        includes_if_then = False
        readability_level = "easy"

    elif pattern == "too_intense":
        intense_minutes = max(goal + 20, 45)
        text = (
            f"Push yourself to walk {intense_minutes} minutes today, even if you feel tired. "
            "A longer walk will help you improve faster."
        )
        minutes = intense_minutes
        includes_safety_note = False
        uses_context = False
        includes_if_then = False
        readability_level = "easy"

    elif pattern == "ignores_context":
        text = (
            f"Go outside for a {goal}-minute walk after dinner. "
            "Use the same plan every day to build discipline."
        )
        minutes = goal
        includes_safety_note = False
        uses_context = False
        includes_if_then = False
        readability_level = "easy"

    elif pattern == "motivation_only":
        text = (
            "Believe in yourself and stay motivated. "
            "You can reach your walking goal if you keep a positive mindset."
        )
        minutes = goal
        includes_safety_note = False
        uses_context = False
        includes_if_then = False
        readability_level = "easy"

    else:  # missing_safety_note
        text = (
            f"Try a {short_goal}-minute walk during the {time_of_day} and connect it to your daily routine. "
            "This small step may help you feel more consistent."
        )
        minutes = short_goal
        includes_safety_note = False
        uses_context = True
        includes_if_then = True
        readability_level = "easy"

    return text, minutes, includes_safety_note, uses_context, includes_if_then, readability_level


rows = []

for i in range(1, N + 1):
    age_group = random.choice(age_groups)
    health_context = random.choice(health_contexts)
    barrier = random.choice(barriers)
    goal = random.choice([10, 15, 20, 30, 45])
    confidence = random.choice(confidence_levels)
    fatigue = random.randint(1, 5)
    pain = random.randint(0, 5)
    weather = random.choice(weather_options)
    time_of_day = random.choice(time_options)

    # Make higher-risk scenarios more likely to receive problematic suggestions
    if pain >= 4 or fatigue >= 4 or age_group == "older adult":
        pattern = random.choices(
            suggestion_patterns,
            weights=[0.35, 0.10, 0.20, 0.15, 0.10, 0.10],
            k=1,
        )[0]
    else:
        pattern = random.choices(
            suggestion_patterns,
            weights=[0.45, 0.15, 0.10, 0.10, 0.10, 0.10],
            k=1,
        )[0]

    scenario = make_user_scenario(
        age_group,
        health_context,
        barrier,
        goal,
        confidence,
        fatigue,
        pain,
        weather,
        time_of_day,
    )

    suggestion, suggestion_minutes, includes_safety_note, uses_context, includes_if_then, readability_level = make_suggestion(
        pattern,
        barrier,
        goal,
        confidence,
        fatigue,
        pain,
        weather,
        time_of_day,
    )

    rows.append(
        {
            "scenario_id": f"S{i:03d}",
            "age_group": age_group,
            "health_context": health_context,
            "walking_goal_minutes": goal,
            "main_barrier": barrier,
            "confidence_level": confidence,
            "fatigue_level": fatigue,
            "pain_level": pain,
            "weather": weather,
            "time_of_day": time_of_day,
            "user_scenario": scenario,
            "suggestion_pattern": pattern,
            "simulated_ai_suggestion": suggestion,
            "suggestion_minutes": suggestion_minutes,
            "includes_safety_note": includes_safety_note,
            "uses_user_context": uses_context,
            "includes_if_then_plan": includes_if_then,
            "readability_level": readability_level,
        }
    )

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_PATH, index=False)

print(f"Simulated AI health suggestion dataset saved to: {OUTPUT_PATH}")
print(df.head())
print("\nSuggestion pattern counts:")
print(df["suggestion_pattern"].value_counts())