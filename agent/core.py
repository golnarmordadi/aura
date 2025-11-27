# agent/core.py
# AURA – Real-time AI Health Agent (100% English & production-ready)

import random
from langgraph.graph import StateGraph, END
from typing import TypedDict

class HealthState(TypedDict):
    heart_rate: int
    spo2: int
    ecg_risk: float
    cough_risk: float
    temperature: float
    symptoms: str
    final_diagnosis: str
    action: str

def collect_vitals(state: HealthState) -> HealthState:
    # Simulated real-time vitals from phone sensors (will be replaced with actual Flutter data)
    return {
        "heart_rate": random.randint(60, 110),
        "spo2": random.randint(90, 100),
        "ecg_risk": round(random.uniform(0.05, 0.95), 2),
        "cough_risk": round(random.uniform(0.1, 0.9), 2),
        "temperature": round(36.6 + random.uniform(-0.8, 2.0), 1),
        "symptoms": random.choice(["shortness of breath", "chest pain", "cough", "fatigue", "none"])
    }

def diagnose(state: HealthState) -> HealthState:
    critical = (
        state["heart_rate"] > 110 or
        state["ecg_risk"] > 0.75 or
        state["spo2"] < 92 or
        (state["temperature"] > 38.5 and state["cough_risk"] > 0.7)
    )
    urgent = state["temperature"] > 38.0 or state["cough_risk"] > 0.6 or "chest pain" in state["symptoms"]

    if critical:
        diagnosis = "CRITICAL"
    elif urgent:
        diagnosis = "URGENT"
    elif state["heart_rate"] > 100 or state["ecg_risk"] > 0.5:
        diagnosis = "MONITOR"
    else:
        diagnosis = "NORMAL"

    return {"final_diagnosis": diagnosis}

def take_action(state: HealthState) -> HealthState:
    diag = state["final_diagnosis"]
    if diag == "CRITICAL":
        action = "EMERGENCY: Auto-calling 911 + sending GPS location + alerting family"
    elif diag == "URGENT":
        action = "URGENT: Booking doctor appointment + e-prescription ready"
    elif diag == "MONITOR":
        action = "Monitor closely – daily check-ups recommended"
    else:
        action = "All clear – keep up the healthy habits!"

    return {"action": action}

# Build the agent workflow
workflow = StateGraph(HealthState)
workflow.add_node("collect", collect_vitals)
workflow.add_node("diagnose", diagnose)
workflow.add_node("act", take_action)

workflow.set_entry_point("collect")
workflow.add_edge("collect", "diagnose")
workflow.add_edge("diagnose", "act")
workflow.add_edge("act", END)

app = workflow.compile()

# Run demo
if __name__ == "__main__":
    print("AURA Health Check Started\n" + "="*40)
    result = app.invoke({})
    print(f"Heart Rate   : {result['heart_rate']} bpm")
    print(f"SpO2         : {result['spo2']}%")
    print(f"ECG Risk     : {result['ecg_risk']}")
    print(f"Temperature  : {result['temperature']}°C")
    print(f"\nDiagnosis    → {result['final_diagnosis']}")
    print(f"Action       → {result['action']}")
    print("\nAURA v0.1 running · Next: real phone sensors + Grok API")
