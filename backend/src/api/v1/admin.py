from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

from api.v1.scenarios import PROGRESS

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

# Simple admin PIN (prototype)
ADMIN_PIN = "1234"


class ResetPayload(BaseModel):
    staff_id: str


@router.post("/reset")
def admin_reset_progress(
    payload: ResetPayload,
    x_admin_pin: str | None = Header(default=None),
):
    # -----------------------------
    # AUTH CHECK
    # -----------------------------
    if x_admin_pin != ADMIN_PIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin PIN",
        )

    staff_input = payload.staff_id.strip().lower()

    if not staff_input:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing staff_id",
        )

    # -----------------------------
    # ADMIN OVERRIDE MODE
    # -----------------------------
    # Using: 1234 + admin
    if staff_input == "admin":

        if not PROGRESS:
            return {
                "status": "ok",
                "message": "No active user progress to reset"
            }

        # Get most recent active user
        current_user = list(PROGRESS.keys())[-1]

        PROGRESS[current_user] = {
        "domains": {},
         "score": 0,
         "completed": [],
        }

        return {
            "status": "ok",
            "message": f"Progress reset for active user: {current_user}"
        }

    # -----------------------------
    # MANUAL USER RESET (fallback)
    # -----------------------------
    for key in list(PROGRESS.keys()):
        if key.lower() == staff_input:
            PROGRESS[key] = {
            "domains": {},
            "score": 0,
            "completed": [],
            }
            return {
                "status": "ok",
                "message": f"Progress reset for staff_id={key}"
            }

    # -----------------------------
    # NOTHING FOUND
    # -----------------------------
    return {
        "status": "ok",
        "message": "No matching user found (nothing reset)"
    }