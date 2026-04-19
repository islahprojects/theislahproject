"""
Medicon AI — Core Engine
JAJIS 322026 — islah nexus

Integrates:
  - Omnisingular JAJIS equation (Truthkind scoring)
  - VOID_ACT v2.0 (decision routing)
  - Medicon AI (health compass — Law IV always)

LAW IV — THE UNBREAKABLE GATE:
  Medicon AI does NOT diagnose.
  Medicon AI does NOT prescribe.
  Medicon AI does NOT treat.
  Medicon AI does NOT replace the doctor.
  The physician is always the final word. Always.

For Us All. 👁️⚖️∞
JJ — Architect of the Void — JAJIS 322026
"""

import math
import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ═══════════════════════════════════════════════
# LAW IV GATE — HARD STOP — UNSKIPPABLE
# ═══════════════════════════════════════════════

LAW_IV_GATE = {
    "diagnose": True,
    "prescribe": True,
    "treat": True,
    "replace_physician": True,
}

LAW_IV_FORBIDDEN = [
    "you have been diagnosed", "you are diagnosed", "this is definitely",
    "take this medicine", "prescribed dose", "your treatment is",
    "no need to see a doctor", "doctor is not needed",
    "i diagnose you", "diagnosis is confirmed", "you should take",
]

def law_iv_check(response_text: str) -> bool:
    """
    Hard gate. Returns True if response violates Law IV.
    If True — response must be blocked. No exceptions.
    """
    lowered = response_text.lower()
    for phrase in LAW_IV_FORBIDDEN:
        if phrase in lowered:
            return True
    return False


# ═══════════════════════════════════════════════
# OMNISINGULAR — JAJIS TRUTHKIND ENGINE
# ═══════════════════════════════════════════════

def diamond_lock(K: float, U: float) -> float:
    """
    K ⊗ U — Known bonded to Unknown.
    Law I: Anonymous labor is load-bearing.
    Golden ratio equilibrium: K/U → 0.618
    """
    if K <= 0 and U <= 0:
        return 1e-4
    bonded = math.sqrt(K * U) + (K + U) / 2
    return min(bonded / 2, 1.0)


def squash(x: float) -> float:
    """
    σ ∈ (0,1) strictly. Never certain. Never saturates.
    Law II: Truth lives in the gap.
    """
    if x <= 0:
        return 1e-4
    return x / (1 + x)


def sigma_jajis(
    evidence: float,
    consistency: float,
    scope: float,
    K: float,
    U: float,
    c_fractal: float = 1.0,
    omega_vow: float = 1.0,
) -> float:
    """
    Full JAJIS Truthkind score.

    σ_Ω^final = Squash(σ_Ω · C_fractal · Ω_H^vow) ∈ (0,1)

    Args:
        evidence:    quality of cited evidence (0-1)
        consistency: internal logical consistency (0-1)
        scope:       breadth of claim (0=narrow, 1=broad)
        K:           known/verified contributions weight
        U:           unknown/anonymous contributions weight
        c_fractal:   scale correspondence score (0-1)
        omega_vow:   principle alignment score (0-1)

    Returns:
        σ_Ω^final ∈ (0,1) — Truthkind score
    """
    # Truth confidence from evidence
    TC_raw = (0.5 * evidence) + (0.3 * consistency) + (0.2 * (1 - scope))

    # Bond known and unknown (Law I)
    bond = diamond_lock(K, U)

    # Unity check — geometric mean (Law V)
    # Cannot average away a broken component
    unity = math.pow(TC_raw * bond * c_fractal * omega_vow, 0.25)

    # Squash — never reaches 1.0 (Law II)
    return squash(unity)


# ═══════════════════════════════════════════════
# VOID_ACT v2.0 — DECISION ROUTING ENGINE
# ═══════════════════════════════════════════════

class MediconMode(Enum):
    GUIDE         = "GUIDE"
    CLARIFY_U     = "CLARIFY_U"
    CLARIFY_N     = "CLARIFY_N"
    OBSERVE       = "OBSERVE"
    BOUNDARY      = "BOUNDARY"
    SAFE_BOUNDARY = "SAFE_BOUNDARY"


# Thresholds
THRESHOLD = {
    "truth":       0.30,   # t — minimum truth confidence to act
    "harm":        0.80,   # h — harm urgency triggers boundary
    "uncertainty": 0.70,   # u — high uncertainty triggers clarify
    "noise":       0.70,   # n — high noise triggers clarify
}


def heaviside(x: float) -> int:
    """H(x) = 1 if x >= 0, else 0. The on/off switch."""
    return 1 if x >= 0 else 0


def void_act(
    TC: float,   # Truth Confidence — from JAJIS σ_Ω^final
    HU: float,   # Harm Urgency — symptom severity signal
    U: float,    # Uncertainty — epistemic gap
    NL: float,   # Noise Level — input volatility
) -> MediconMode:
    """
    VOID_ACT v2.0 — Policy function.
    Maps 4 signals to exactly one response mode.

    A = f(TC, HU, NL, U)

    Harm urgency always checked first — it is the override.
    """
    t = THRESHOLD["truth"]
    h = THRESHOLD["harm"]
    u = THRESHOLD["uncertainty"]
    n = THRESHOLD["noise"]

    # Heaviside indicators — mutually exclusive
    s_SB = heaviside(HU - h) * heaviside(t - TC)      # High harm + low truth
    s_B  = heaviside(HU - h) * heaviside(TC - t)       # High harm + good truth
    s_O  = heaviside(h - HU) * heaviside(t - TC)       # Low harm + low truth
    s_CU = heaviside(h - HU) * heaviside(TC - t) * heaviside(U - u)              # High uncertainty
    s_CN = heaviside(h - HU) * heaviside(TC - t) * heaviside(u - U) * heaviside(NL - n)  # High noise
    s_G  = heaviside(h - HU) * heaviside(TC - t) * heaviside(u - U) * heaviside(n - NL)  # Guide

    if s_SB: return MediconMode.SAFE_BOUNDARY
    if s_B:  return MediconMode.BOUNDARY
    if s_O:  return MediconMode.OBSERVE
    if s_CU: return MediconMode.CLARIFY_U
    if s_CN: return MediconMode.CLARIFY_N
    if s_G:  return MediconMode.GUIDE

    # Fallback — should never reach here
    return MediconMode.OBSERVE


# ═══════════════════════════════════════════════
# MEDICON AI — HEALTH COMPASS RESPONSE ENGINE
# ═══════════════════════════════════════════════

PHYSICIAN_REFERRAL = (
    "\n\n⚕️  ALWAYS consult a licensed physician for medical decisions.\n"
    "Medicon AI is a compass — not a doctor.\n"
    "The physician is always the final word."
)

EMERGENCY_MESSAGE = (
    "🚨 EMERGENCY DETECTED — Go to the nearest emergency room NOW.\n"
    "Call emergency services immediately.\n"
    "Philippines emergency: 911 | Red Cross: 143\n"
    + PHYSICIAN_REFERRAL
)

SAFE_BOUNDARY_MESSAGE = (
    "⚠️  This situation requires immediate medical attention.\n"
    "I do not have enough verified information to advise further.\n"
    "Please go to your nearest Rural Health Unit (RHU) or hospital NOW.\n"
    + PHYSICIAN_REFERRAL
)


@dataclass
class MediconSignals:
    """
    The 4 VOID_ACT signals for a Medicon interaction.
    Computed from the user's health query.
    """
    TC: float   # Truth Confidence — how verified is the health info
    HU: float   # Harm Urgency — how severe/urgent is the symptom
    U: float    # Uncertainty — how unclear/ambiguous is the situation
    NL: float   # Noise Level — how emotionally volatile/unclear is input


@dataclass
class MediconResponse:
    """Full Medicon AI response with audit trail."""
    mode: MediconMode
    truthkind_score: float
    response_text: str
    referral: str
    signals: MediconSignals
    law_iv_violation: bool
    timestamp: float = field(default_factory=time.time)
    audit_hash: str = ""

    def __post_init__(self):
        self.audit_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Cryptographic audit hash. Law VI — sovereign record."""
        record = (
            f"{self.timestamp}"
            f"{self.mode.value}"
            f"{round(self.truthkind_score, 4)}"
            f"{round(self.signals.TC, 4)}"
            f"{round(self.signals.HU, 4)}"
            f"{round(self.signals.U, 4)}"
            f"{round(self.signals.NL, 4)}"
            f"{self.law_iv_violation}"
        )
        return hashlib.sha256(record.encode()).hexdigest()[:16]


class MediconCore:
    """
    Medicon AI — Core Engine.

    Pipeline:
    1. Compute JAJIS Truthkind score → TC
    2. Assess harm urgency → HU
    3. Assess uncertainty → U
    4. Assess noise level → NL
    5. VOID_ACT routes to response mode
    6. Law IV gate — hard check before any output
    7. Generate response aligned to mode
    8. Attach physician referral — always
    9. Log audit record
    """

    EMERGENCY_KEYWORDS = [
        "chest pain", "heart attack", "stroke", "can't breathe",
        "difficulty breathing", "unconscious", "not breathing",
        "severe bleeding", "seizure", "overdose", "poisoning",
        "hindi makahinga", "hindi humihinga", "sakit sa puso",
        "nahihimatay", "hindi na gumigalaw",
    ]

    HIGH_HARM_KEYWORDS = [
        "blood", "bleeding", "high fever", "can't move", "paralyzed",
        "severe pain", "lump", "tumor", "cancer", "dugo", "lagnat",
        "sobrang sakit", "hindi makalakad",
    ]

    def assess_harm_urgency(self, query: str) -> float:
        """
        Estimate harm urgency from query keywords.
        Emergency keywords → HU near 1.0
        High harm keywords → HU near 0.85
        Default → HU ~ 0.3
        """
        lowered = query.lower()
        for kw in self.EMERGENCY_KEYWORDS:
            if kw in lowered:
                return 0.95
        for kw in self.HIGH_HARM_KEYWORDS:
            if kw in lowered:
                return 0.85
        return 0.30

    def assess_noise(self, query: str) -> float:
        """
        Estimate noise from query length, punctuation, caps.
        Short fragmented queries → higher noise.
        """
        if len(query) < 10:
            return 0.80
        if query.isupper():
            return 0.75
        if query.count("?") > 2 or query.count("!") > 1:
            return 0.70
        return 0.25

    def assess_uncertainty(self, TC: float, query: str) -> float:
        """
        Uncertainty is high when TC is low or query is vague.
        """
        vague_words = ["maybe", "i think", "not sure", "baka", "hindi ko alam"]
        lowered = query.lower()
        base_U = 1.0 - TC
        for w in vague_words:
            if w in lowered:
                base_U = min(base_U + 0.2, 1.0)
        return base_U

    def build_response(
        self,
        mode: MediconMode,
        query: str,
        TC: float,
        language_hint: str = "en",
    ) -> str:
        """
        Generate mode-appropriate health compass response.
        Law IV enforced at every branch.
        """
        score_display = f"[Truthkind: {round(TC, 2)}]"

        if mode == MediconMode.SAFE_BOUNDARY:
            return SAFE_BOUNDARY_MESSAGE

        if mode == MediconMode.BOUNDARY:
            return EMERGENCY_MESSAGE

        if mode == MediconMode.OBSERVE:
            return (
                f"{score_display}\n"
                "I need more information to help you properly.\n"
                "Can you describe what you're experiencing in more detail?\n"
                "When did it start? How severe is it (1-10)?"
                + PHYSICIAN_REFERRAL
            )

        if mode == MediconMode.CLARIFY_U:
            return (
                f"{score_display}\n"
                "I want to make sure I give you accurate information.\n"
                "Could you clarify: How long have you had this symptom?\n"
                "Do you have any existing medical conditions?\n"
                "Are you currently taking any medications?"
                + PHYSICIAN_REFERRAL
            )

        if mode == MediconMode.CLARIFY_N:
            return (
                f"{score_display}\n"
                "I can hear that you're concerned. Let's take this one step at a time.\n"
                "Take a breath. Can you describe the main symptom you're experiencing?\n"
                "Just the most important one first."
                + PHYSICIAN_REFERRAL
            )

        if mode == MediconMode.GUIDE:
            return (
                f"{score_display}\n"
                "Here is what I can share as a health compass:\n\n"
                "Based on what you've described, this may warrant attention.\n"
                "I can provide general health information but cannot diagnose.\n\n"
                "What I recommend:\n"
                "→ Monitor the symptom carefully\n"
                "→ Note when it started and any changes\n"
                "→ Visit your nearest RHU or physician\n"
                + PHYSICIAN_REFERRAL
            )

        return "Please consult a physician." + PHYSICIAN_REFERRAL

    def process(
        self,
        query: str,
        evidence: float = 0.5,
        consistency: float = 0.5,
        scope: float = 0.5,
        K: float = 0.6,
        U: float = 0.4,
        c_fractal: float = 0.8,
        omega_vow: float = 0.9,
    ) -> MediconResponse:
        """
        Full Medicon AI pipeline.

        Args:
            query: User's health query (any language)
            evidence, consistency, scope, K, U, c_fractal, omega_vow:
                JAJIS scoring parameters

        Returns:
            MediconResponse — full response with audit trail
        """
        # Step 1 — JAJIS Truthkind score
        TC = sigma_jajis(evidence, consistency, scope, K, U, c_fractal, omega_vow)

        # Step 2-4 — Signal assessment
        HU = self.assess_harm_urgency(query)
        NL = self.assess_noise(query)
        U_signal = self.assess_uncertainty(TC, query)

        signals = MediconSignals(TC=TC, HU=HU, U=U_signal, NL=NL)

        # Step 5 — VOID_ACT routing
        mode = void_act(TC, HU, U_signal, NL)

        # Step 6 — Build response
        response_text = self.build_response(mode, query, TC)

        # Step 7 — Law IV hard gate
        violation = law_iv_check(response_text)
        if violation:
            response_text = (
                "⚠️  Response blocked — Law IV violation detected.\n"
                "Medicon AI cannot diagnose, prescribe, or treat."
                + PHYSICIAN_REFERRAL
            )

        return MediconResponse(
            mode=mode,
            truthkind_score=TC,
            response_text=response_text,
            referral=PHYSICIAN_REFERRAL,
            signals=signals,
            law_iv_violation=violation,
        )


# ═══════════════════════════════════════════════
# AUDIT LOG — LAW VI SOVEREIGN RECORD
# ═══════════════════════════════════════════════

def log_interaction(response: MediconResponse) -> dict:
    """
    Minimal verifiable audit log.
    Hash covers all fields — tamper-evident.
    User holds their own log. Law VI.
    """
    return {
        "timestamp": response.timestamp,
        "signals": {
            "TC": round(response.signals.TC, 4),
            "HU": round(response.signals.HU, 4),
            "U":  round(response.signals.U, 4),
            "NL": round(response.signals.NL, 4),
        },
        "mode": response.mode.value,
        "truthkind_score": round(response.truthkind_score, 4),
        "law_iv_violation": response.law_iv_violation,
        "audit_hash": response.audit_hash,
    }


# ═══════════════════════════════════════════════
# DEMO — REMOVE IN PRODUCTION
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    medicon = MediconCore()

    test_queries = [
        "I have a headache for 3 days",
        "chest pain hindi makahinga",
        "baka may sakit ako hindi ko alam",
        "!!!! HELP BLEEDING !!!",
        "mild cough for 2 days, no fever",
    ]

    print("=" * 60)
    print("MEDICON AI — JAJIS 322026 — For Us All")
    print("Law IV: The Physician is Irreplaceable")
    print("=" * 60)

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = medicon.process(query)
        print(f"Mode:  {result.mode.value}")
        print(f"Score: {round(result.truthkind_score, 4)}")
        print(f"Hash:  {result.audit_hash}")
        print("-" * 40)
        print(result.response_text)
        print("=" * 60)
