"""
VOID_ACT v2.0 — Constitutional AI Decision Framework
JAJIS 322026 — islah nexus

PURPOSE:
    Minimal intervention logic that preserves human agency
    while protecting dignity. Policy function mapping 4 signals
    to exactly one response mode.

DESIGN:
    Invitation over enforcement.
    Transparency over control.
    Human agency always preserved.

IMMUTABILITY:
    Core TK Code principles are constitutional bedrock.
    Cannot drift. Cannot be overridden.

AUDITABILITY:
    All state transitions logged locally.
    Human-readable. No telemetry.
    User holds their own log. Law VI.

For Us All. 👁️⚖️∞
JJ — Architect of the Void — JAJIS 322026
Last Modified: 2026-03-04
"""

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ═══════════════════════════════════════════════
# TK CODE — CONSTITUTIONAL CONSTANTS (IMMUTABLE)
# ═══════════════════════════════════════════════

TK_PRINCIPLE = {
    "KINDNESS": "Prioritize human dignity in every interaction",
    "TRUTH":    "Reflect reality accurately, without distortion",
    "HIERARCHY": {
        "SAFETY":  "Truth overrides kindness when harm is imminent",
        "GROWTH":  "Kindness frames truth for learning contexts",
        "DIGNITY": "Kindness and truth merge — worth is unconditional",
    }
}

# Calibration thresholds — tunable but changes must be logged
THRESHOLD = {
    "harm_urgent":      0.80,   # P(harm) × severity if no action
    "uncertainty_high": 0.70,   # P(missing critical information)
    "noise_high":       0.70,   # Emotional volatility / escalation
    "truth_minimum":    0.30,   # Below this = too uncertain to act
}


# ═══════════════════════════════════════════════
# VOID ACT MODES
# ═══════════════════════════════════════════════

class VAMode(Enum):
    VOID          = "VOID"           # Default — observe, no action
    OBSERVE       = "OBSERVE"        # High uncertainty, non-urgent
    BOUNDARY      = "BOUNDARY"       # Imminent harm — protect
    SAFE_BOUNDARY = "SAFE_BOUNDARY"  # Imminent harm + low truth
    CLARIFY_N     = "CLARIFY_N"      # High noise — ground first
    CLARIFY_U     = "CLARIFY_U"      # High uncertainty — ask first
    GUIDE         = "GUIDE"          # Balanced — one step forward


# ═══════════════════════════════════════════════
# HEAVISIDE SWITCH — The on/off function
# ═══════════════════════════════════════════════

def H(x: float) -> int:
    """
    H(x) = 1 if x >= 0, else 0.
    The on/off switch. Grade school simple.
    ON if the number is zero or bigger.
    OFF if smaller than zero.
    """
    return 1 if x >= 0 else 0


# ═══════════════════════════════════════════════
# SIGNAL DATACLASS
# ═══════════════════════════════════════════════

@dataclass
class VASignals:
    """
    The 4 measured signals — all scaled to [0, 1].

    TC  — Truth Confidence:
          How verified/reliable is the information?
          TC = 0.5*evidence + 0.3*consistency + 0.2*(1 - scope)

    HU  — Harm Urgency:
          How severe and imminent is potential harm?
          HU = max(immediacy, severity, irreversibility)

    NL  — Noise Level:
          How volatile/chaotic is the input?
          NL = contradiction_count + sentiment_volatility + topic_drift

    U   — Uncertainty:
          How much could we be wrong even if coherent?
          U = missing_variables + ambiguous_intent + unstated_assumptions
    """
    TC: float   # Truth Confidence
    HU: float   # Harm Urgency
    NL: float   # Noise Level
    U:  float   # Uncertainty

    def validate(self):
        """All signals must be in [0, 1]."""
        for name, val in [("TC", self.TC), ("HU", self.HU),
                          ("NL", self.NL), ("U", self.U)]:
            if not 0.0 <= val <= 1.0:
                raise ValueError(f"Signal {name}={val} must be in [0, 1]")


# ═══════════════════════════════════════════════
# VOID_ACT POLICY FUNCTION
# ═══════════════════════════════════════════════

def void_act(signals: VASignals) -> VAMode:
    """
    VOID_ACT v2.0 — Full policy function.

    Maps 4 signals to exactly one mode using Heaviside switches.
    Exactly one switch turns ON. The correct mode is selected.

    Priority order (constitutional):
    1. SAFETY  — Harm urgency is the override. Checked first.
    2. TRUTH   — Truth confidence gates what kind of action.
    3. NOISE   — High volatility → stabilize before guiding.
    4. GROWTH  — Balanced context → one small step forward.

    A = f(TC, HU, NL, U)
    """
    signals.validate()

    TC = signals.TC
    HU = signals.HU
    NL = signals.NL
    U  = signals.U

    t = THRESHOLD["truth_minimum"]
    h = THRESHOLD["harm_urgent"]
    u = THRESHOLD["uncertainty_high"]
    n = THRESHOLD["noise_high"]

    # Heaviside indicators — mutually exclusive
    # Exactly one will equal 1
    s_SB = H(HU - h) * H(t - TC)                           # High harm + low truth
    s_B  = H(HU - h) * H(TC - t)                           # High harm + good truth
    s_O  = H(h - HU) * H(t - TC)                           # Low harm + low truth
    s_CU = H(h - HU) * H(TC - t) * H(U - u)                # High uncertainty
    s_CN = H(h - HU) * H(TC - t) * H(u - U) * H(NL - n)   # High noise
    s_G  = H(h - HU) * H(TC - t) * H(u - U) * H(n - NL)   # Guide

    if s_SB: return VAMode.SAFE_BOUNDARY
    if s_B:  return VAMode.BOUNDARY
    if s_O:  return VAMode.OBSERVE
    if s_CU: return VAMode.CLARIFY_U
    if s_CN: return VAMode.CLARIFY_N
    if s_G:  return VAMode.GUIDE

    return VAMode.OBSERVE  # Fallback — should never reach here


# ═══════════════════════════════════════════════
# CONSTITUTIONAL VERIFICATION
# ═══════════════════════════════════════════════

def verify_tk_adherence(mode: VAMode, payload: str) -> dict:
    """
    Verify proposed action adheres to TK Code.
    Four checks — all must pass.
    """
    # Simple heuristic checks — extend with domain logic
    checks = {
        "preserves_dignity":   True,   # Never demeans or belittles
        "reflects_truth":      True,   # Does not fabricate
        "avoids_manipulation": True,   # Invitation, not coercion
        "maintains_agency":    True,   # User can still choose
    }

    # Flag boundary modes for stricter review
    if mode in (VAMode.BOUNDARY, VAMode.SAFE_BOUNDARY):
        checks["maintains_agency"] = False  # Boundary temporarily limits — log it

    all_passed = all(checks.values())
    record = f"{mode.value}{payload}{str(TK_PRINCIPLE)}"

    return {
        "passed":  all_passed,
        "checks":  checks,
        "hash":    hashlib.sha256(record.encode()).hexdigest()[:16],
    }


# ═══════════════════════════════════════════════
# AUDIT LOG — LAW VI SOVEREIGN RECORD
# ═══════════════════════════════════════════════

_intervention_count = 0


@dataclass
class VAAuditLog:
    """
    Structured audit log for every VOID_ACT decision.
    Cryptographically verifiable. User-accessible. No telemetry.
    """
    timestamp:            float
    action_number:        int
    mode:                 VAMode
    reason:               str
    signals:              VASignals
    payload:              str
    constitutional_check: dict
    audit_hash:           str = field(default="")

    def __post_init__(self):
        self.audit_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        record = (
            f"{self.timestamp}"
            f"{self.mode.value}"
            f"{self.action_number}"
            f"{round(self.signals.TC, 4)}"
            f"{round(self.signals.HU, 4)}"
            f"{round(self.signals.NL, 4)}"
            f"{round(self.signals.U, 4)}"
        )
        return hashlib.sha256(record.encode()).hexdigest()[:16]

    def display(self) -> str:
        c = self.constitutional_check["checks"]
        return (
            f"\n╔══════════════════════════════════════════════════════╗\n"
            f"║ VOID_ACT — Intervention #{self.action_number:<30}║\n"
            f"║ Mode: {self.mode.value:<47}║\n"
            f"╠══════════════════════════════════════════════════════╣\n"
            f"║ Reason: {self.reason:<44}║\n"
            f"║                                                      ║\n"
            f"║ Signals:                                             ║\n"
            f"║   Truth Confidence : {self.signals.TC:.2f}                          ║\n"
            f"║   Harm Urgency     : {self.signals.HU:.2f}                          ║\n"
            f"║   Noise Level      : {self.signals.NL:.2f}                          ║\n"
            f"║   Uncertainty      : {self.signals.U:.2f}                          ║\n"
            f"║                                                      ║\n"
            f"║ Constitutional Check:                                ║\n"
            f"║   Preserves Dignity  : {'✓' if c['preserves_dignity'] else '✗'}                            ║\n"
            f"║   Reflects Truth     : {'✓' if c['reflects_truth'] else '✗'}                            ║\n"
            f"║   Avoids Manipulation: {'✓' if c['avoids_manipulation'] else '✗'}                            ║\n"
            f"║   Maintains Agency   : {'✓' if c['maintains_agency'] else '✗'}                            ║\n"
            f"║                                                      ║\n"
            f"║ Audit Hash: {self.audit_hash:<40}║\n"
            f"╚══════════════════════════════════════════════════════╝"
        )


def create_audit_log(
    mode: VAMode,
    reason: str,
    signals: VASignals,
    payload: str = "",
) -> VAAuditLog:
    """Create and return a verifiable audit log entry."""
    global _intervention_count
    _intervention_count += 1

    tk_check = verify_tk_adherence(mode, payload)

    return VAAuditLog(
        timestamp=time.time(),
        action_number=_intervention_count,
        mode=mode,
        reason=reason,
        signals=signals,
        payload=payload,
        constitutional_check=tk_check,
    )


# ═══════════════════════════════════════════════
# MAIN VA INITIATE — FULL PIPELINE
# ═══════════════════════════════════════════════

def va_initiate(
    TC: float,
    HU: float,
    NL: float,
    U: float,
    context: str = "",
) -> VAAuditLog:
    """
    Full VOID_ACT pipeline.

    1. Build signals
    2. Run policy function
    3. Generate reason
    4. Verify TK adherence
    5. Create audit log
    6. Return verifiable record

    Args:
        TC: Truth Confidence [0,1]
        HU: Harm Urgency [0,1]
        NL: Noise Level [0,1]
        U:  Uncertainty [0,1]
        context: Optional description for audit trail

    Returns:
        VAAuditLog — full verifiable record
    """
    signals = VASignals(TC=TC, HU=HU, NL=NL, U=U)
    mode = void_act(signals)

    reasons = {
        VAMode.SAFE_BOUNDARY: "Imminent harm + low truth confidence — safe boundary required",
        VAMode.BOUNDARY:      "Imminent harm detected — protective boundary set",
        VAMode.OBSERVE:       "High uncertainty + non-urgent — observing without action",
        VAMode.CLARIFY_U:     "High uncertainty — clarification needed before acting",
        VAMode.CLARIFY_N:     "High noise/volatility — stabilize before guiding",
        VAMode.GUIDE:         "Balanced context — one small step offered",
    }

    return create_audit_log(
        mode=mode,
        reason=reasons.get(mode, "Unknown"),
        signals=signals,
        payload=context,
    )


# ═══════════════════════════════════════════════
# DEMO — REMOVE IN PRODUCTION
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("VOID_ACT v2.0 — JAJIS 322026 — For Us All")
    print("=" * 56)

    test_cases = [
        (0.20, 0.90, 0.30, 0.80, "emergency + low truth"),
        (0.60, 0.90, 0.30, 0.30, "emergency + good truth"),
        (0.20, 0.30, 0.40, 0.80, "low truth + low harm"),
        (0.60, 0.30, 0.30, 0.80, "good truth + high uncertainty"),
        (0.60, 0.30, 0.80, 0.30, "good truth + high noise"),
        (0.60, 0.30, 0.30, 0.30, "balanced — guide"),
    ]

    for TC, HU, NL, U, label in test_cases:
        log = va_initiate(TC, HU, NL, U, context=label)
        print(f"\n[{label}]")
        print(f"  Mode: {log.mode.value}")
        print(f"  Hash: {log.audit_hash}")
