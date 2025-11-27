# agent/core.py
import random  # برای دمو — بعداً از سنسور واقعی
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import neurokit2 as nk  # برای ECG ساده
import numpy as np

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
    # شبیه‌سازی داده از گوشی (بعداً از Flutter می‌آید)
    ecg_signal = nk.ecg_simulate(duration=10, heart_rate=80)  # سیگنال ECG نمونه
    hr, info = nk.ecg_peaks(ecg_signal)[0:2]
    heart_rate = len(hr) / 10  # bpm
    
    return {
        "heart_rate": int(heart_rate + random.uniform(-5, 5)),  # ۷۵-۸۵
        "spo2": int(95 + random.uniform(-3, 3)),  # ۹۲-۹۸
        "ecg_risk": random.uniform(0.1, 0.9),  # ریسک آریتمی
        "cough_risk": random.uniform(0.2, 0.8),  # ریسک عفونت
        "temperature": 36.5 + random.uniform(-0.5, 1.5),  # ۳۶-۳۸
        "symptoms": "تنگی نفس خفیف"  # از کاربر ورودی
    }

def diagnose(state: HealthState) -> HealthState:
    # prompt برای Grok/Claude (فعلاً شبیه‌سازی — بعداً API واقعی)
    risks = {
        "heart": state['heart_rate'] > 100 or state['ecg_risk'] > 0.7,
        "oxygen": state['spo2'] < 92,
        "fever": state['temperature'] > 38,
        "cough": state['cough_risk'] > 0.6
    }
    
    if any([risks['heart'], risks['oxygen'] and risks['fever']]):
        diagnosis = "CRITICAL"  # حمله قلبی یا سپسیس
    elif risks['cough'] or risks['fever']:
        diagnosis = "URGENT"  # عفونت تنفسی
    else:
        diagnosis = "MONITOR"  # پیگیری
    
    return {"final_diagnosis": diagnosis}

def take_action(state: HealthState) -> HealthState:
    if state["final_diagnosis"] == "CRITICAL":
        action = "🚨 تماس خودکار با ۱۱۵ + ارسال GPS + هشدار به خانواده"
    elif state["final_diagnosis"] == "URGENT":
        action = "⚠️ نوبت آنلاین دکتر + سفارش دارو از داروخانه"
    else:
        action = "✅ همه چیز نرمال — توصیه: ۸ ساعت خواب + ورزش روزانه"
    
    return {"action": action}

# ساخت گراف Agent
workflow = StateGraph(HealthState)
workflow.add_node("collect", collect_vitals)
workflow.add_node("diagnose", diagnose)
workflow.add_node("act", take_action)

workflow.set_entry_point("collect")
workflow.add_edge("collect", "diagnose")
workflow.add_edge("diagnose", "act")
workflow.add_edge("act", END)

app = workflow.compile()

# تست دمو
if __name__ == "__main__":
    result = app.invoke({})
    print("نتایج چک‌آپ AURA:")
    print(f"تشخیص: {result['final_diagnosis']}")
    print(f"اقدام: {result['action']}")
    print("دمو کامل شد! حالا سنسورهای واقعی رو ادغام کن.")
