from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from api.v1.domains import DOMAINS

router = APIRouter(prefix="/api/v1", tags=["scenarios"])

PASS_MARK_PERCENT = 70

SCENARIOS = [
    # -------------------------
    # PHISHING (3)
    # -------------------------
    {
    "id": "phish_001",
    "domain": "phishing",
    "title": "Suspicious Email Link",
    "difficulty": "easy",
    "question": "You receive an email saying your Microsoft password will expire today. It asks you to click a link to verify your account. What should you do?",
    "options": [
        {"id": "a", "text": "Do not click the link. Use the official Microsoft/IT portal (or your known bookmark) to check your account, and report the email using the company process."},
        {"id": "b", "text": "Check the sender address carefully and decide based on how convincing the email looks."},
        {"id": "c", "text": "Click the link and sign in quickly to avoid losing access."},
        {"id": "d", "text": "Forward it to colleagues to warn them."},
    ],
    "answer": "a",
    "explanation": "Urgent password-expiry emails are a common phishing trick. Don’t click unknown links—use official portals/bookmarks and report suspicious messages via the company process.",
    "points": 10,
},
{
    "id": "phish_002",
    "domain": "phishing",
    "title": "DocuSign / Shared File Trap",
    "difficulty": "medium",
    "question": "You receive an email saying a document has been shared with you and you must ‘review it today’. The button says ‘Open document’. You were not expecting this. What is the safest action?",
    "options": [
        {"id": "a", "text": "Click the button to see what the document is."},
        {"id": "b", "text": "Reply to the sender and wait for their response, then click the button if they confirm."},
        {"id": "c", "text": "Forward it to a colleague to see if they received it too."},
        {"id": "d", "text": "Do not click. Open DocuSign/SharePoint via a trusted route (known bookmark/portal), or verify with the sender using a known contact method. Report it if suspicious."},
    ],
    "answer": "d",
    "explanation": "Unexpected shared-file/signing emails are common phishing lures. Don’t use the email button—verify via trusted portals/bookmarks or known contacts, then report if suspicious.",
    "points": 20,
},
{
    "id": "phish_003",
    "domain": "phishing",
    "title": "QR Code ‘Secure Login’ (Quishing)",
    "difficulty": "hard",
    "question": "You see a poster in the office kitchen with a QR code: 'Scan to re-verify your Microsoft login (required today)'. A colleague says IT put them up. What should you do?",
    "options": [
        {"id": "a", "text": "Scan it — it’s in the office so it’s safe."},
        {"id": "b", "text": "Scan it and check the URL carefully before doing anything, since Microsoft pages are easy to recognise."},
        {"id": "c", "text": "Take a photo and share it in a group chat to warn people."},
        {"id": "d", "text": "Do not scan. Check for an official internal announcement/service portal entry, or verify via a known IT/helpdesk contact method. Report the poster if it isn’t verified."},
    ],
    "answer": "d",
    "explanation": "QR-code phishing (“quishing”) hides the real link and can bypass email filters. Don’t scan random QR codes—verify through official channels and report unverified posters.",
    "points": 30,
},
    # -------------------------
    # PASSWORDS (3)
    # -------------------------
    {
    "id": "pwd_001",
    "domain": "passwords",
    "title": "Weak Password Reuse",
    "difficulty": "easy",
    "question": "You use the same password for your work email and a shopping website. The shopping site is breached. What is the main risk?",
    "options": [
        {"id": "a", "text": "Attackers can try the leaked password on your work email and other services you use (credential stuffing)."},
        {"id": "b", "text": "Only the shopping website is affected because work systems are separate."},
        {"id": "c", "text": "Your antivirus software will block any login attempts automatically."},
        {"id": "d", "text": "Change your shopping password only — your work account can’t be affected."},
    ],
    "answer": "a",
    "explanation": "Password reuse allows credential stuffing, where attackers try leaked passwords on other services like work email. Unique passwords reduce this risk.",
    "points": 10,
},
{
    "id": "pwd_002",
    "domain": "passwords",
    "title": "MFA Fatigue Prompt",
    "difficulty": "medium",
    "question": "You keep receiving repeated Microsoft sign-in prompts asking you to approve a login. You are not trying to sign in. What should you do?",
    "options": [
        {"id": "a", "text": "Approve one request so the prompts stop."},
        {"id": "b", "text": "Ignore the prompts — if you don’t approve them, nothing can happen."},
        {"id": "c", "text": "Check your account later — repeated prompts usually mean a system sync issue."},
        {"id": "d", "text": "Deny the prompts, change your password immediately, and report it to IT/security."},
    ],
    "answer": "d",
    "explanation": "Repeated MFA prompts often mean an attacker already has your password and is trying to force access. Deny the request, reset your password, and report it immediately.",
    "points": 20,
},
{
    "id": "pwd_003",
    "domain": "passwords",
    "title": "Password Manager vs ‘Complex’ Reuse",
    "difficulty": "hard",
    "question": "A colleague says they reuse the same long, complex password everywhere because it’s 'impossible to guess'. Why is this still risky?",
    "options": [
        {"id": "a", "text": "Long passwords eventually expire automatically, which causes access issues."},
        {"id": "b", "text": "Long passwords are usually safe unless the attacker targets you personally."},
        {"id": "c", "text": "If one site is breached, attackers can reuse the password on other services regardless of how complex it is."},
        {"id": "d", "text": "Complex passwords are more likely to be written down."},
    ],
    "answer": "c",
    "explanation": "Password complexity doesn’t help if the password is leaked. Reuse allows credential stuffing across multiple services. Unique passwords (ideally via a password manager) prevent this.",
    "points": 30,
},
    # -------------------------
    # BEC (3)
    # -------------------------
    {
    "id": "bec_001",
    "domain": "bec",
    "title": "Urgent CEO Payment Request",
    "difficulty": "medium",
    "question": "You get an email from the CEO asking you to urgently pay an invoice and keep it confidential. The tone feels unusual. What’s the best action?",
    "options": [
        {"id": "a", "text": "Follow the normal payment process: verify the request using a trusted method (known number/internal directory) and get the required approvals before paying."},
        {"id": "b", "text": "Reply asking the CEO to confirm the request by email since it came from their address."},
        {"id": "c", "text": "Pay it now to keep things moving — you can sort the paperwork afterwards."},
        {"id": "d", "text": "Forward the email to colleagues to check if they’ve seen similar requests."},
    ],
    "answer": "a",
    "explanation": "BEC scams rely on urgency and secrecy. The safest response is to verify via trusted contact details and follow normal approval controls before any payment.",
    "points": 20,
},
{
    "id": "bec_002",
    "domain": "bec",
    "title": "Supplier Bank Details Change",
    "difficulty": "medium",
    "question": "A supplier emails saying their bank details have changed and asks you to use the new account for the next payment. The email looks professional. What should you do?",
    "options": [
        {"id": "a", "text": "Update the bank details straight away so the next payment isn’t late."},
        {"id": "b", "text": "Verify the change using a trusted method (known phone number/contract contact/approved process) before updating anything."},
        {"id": "c", "text": "Reply asking them to confirm the change by email and wait for a written response before updating the details."},
        {"id": "d", "text": "Make a small test payment first to check the account is correct."},
    ],
    "answer": "b",
    "explanation": "Bank detail change requests are a classic BEC tactic. Always verify via trusted contact info and follow your official supplier-change process before changing payment details.",
    "points": 20,
},
{
    "id": "bec_003",
    "domain": "bec",
    "title": "Invoice Thread Hijack",
    "difficulty": "hard",
    "question": "You receive a reply in an existing email thread about an invoice you’ve been discussing for weeks. The reply contains updated bank details and looks consistent with the thread. What’s the safest action?",
    "options": [
        {"id": "a", "text": "Pay it — it’s in the same email thread so it must be legitimate."},
        {"id": "b", "text": "Reply in the same email thread asking them to reconfirm the bank details, then proceed if they respond."},
        {"id": "c", "text": "Ask a colleague if it looks real, then pay if they agree."},
        {"id": "d", "text": "Treat it as high-risk: verify the bank change using a trusted method (known phone number/supplier master data/approved process) before paying."},
    ],
    "answer": "d",
    "explanation": "Attackers can hijack real email threads. Any bank detail change must be verified through trusted channels and your approved process before payment.",
    "points": 30,
},
    # -------------------------
    # CREDENTIAL THEFT (3)
    # -------------------------
    {
    "id": "cred_001",
    "domain": "credential_theft",
    "title": "Unexpected MFA Prompt",
    "difficulty": "easy",
    "question": "You receive a Microsoft sign-in approval prompt on your phone, but you are not trying to log in. What should you do?",
    "options": [
        {"id": "a", "text": "Deny the prompt, secure your account by changing your password, and follow your organisation’s reporting process."},
        {"id": "b", "text": "Approve it in case it’s a system check and see if anything unusual happens."},
        {"id": "c", "text": "Ignore it for now — if it’s a real issue, IT will block the attempt automatically."},
        {"id": "d", "text": "Approve it, then sign out of all devices later just to be safe."},
    ],
    "answer": "a",
    "explanation": "Unexpected MFA prompts often indicate someone has your password. Deny the request, secure your account immediately, and report it through the correct process.",
    "points": 10,
},
{
    "id": "cred_002",
    "domain": "credential_theft",
    "title": "Shared Account Shortcut",
    "difficulty": "medium",
    "question": "A colleague asks for your login because they can’t access a system and need to 'just get something done quickly'. What is the safest response?",
    "options": [
        {"id": "a", "text": "Log in for them briefly so they can complete the task, then log out straight away."},
        {"id": "b", "text": "Do not share credentials. Help them by using the proper access request process or directing them to IT."},
        {"id": "c", "text": "Share your login just this once and change it afterwards."},
        {"id": "d", "text": "Ask them to email the request so you have proof before sharing."},
    ],
    "answer": "b",
    "explanation": "Sharing credentials breaks accountability and security controls. Access should always be granted through approved processes so activity is traceable and secure.",
    "points": 20,
},
{
    "id": "cred_003",
    "domain": "credential_theft",
    "title": "Fake Helpdesk Callback",
    "difficulty": "hard",
    "question": "You get a call from 'IT Support' saying they detected suspicious login attempts and need you to confirm a code they just sent to your phone to 'secure your account'. What should you do?",
    "options": [
        {"id": "a", "text": "Give them the code quickly so they can block the attacker."},
        {"id": "b", "text": "Ask them to confirm some basic details about you, then continue the call if they sound convincing."},
        {"id": "c", "text": "Hang up immediately and contact IT using a known internal number or official helpdesk method."},
        {"id": "d", "text": "Tell them you’ll send the code by email instead."},
    ],
    "answer": "c",
    "explanation": "Verification codes must never be shared. This is a common social-engineering attack. Always hang up and contact IT using trusted contact details.",
    "points": 30,
},
    # -------------------------
    # MALWARE & RANSOMWARE (3)
    # -------------------------
    {
    "id": "mal_001",
    "domain": "malware",
    "title": "Invoice Attachment Surprise",
    "difficulty": "easy",
    "question": "You receive an email that looks like it’s from a supplier with an 'urgent invoice' attached. You weren’t expecting it. What should you do first?",
    "options": [
        {"id": "a", "text": "Check the sender using a trusted contact method before opening the attachment and follow your organisation’s reporting process if it seems suspicious."},
        {"id": "b", "text": "Open the attachment carefully to see if it looks genuine."},
        {"id": "c", "text": "Forward it to Finance without opening it, assuming they will know if it’s legitimate."},
        {"id": "d", "text": "Download it and scan it later when you have time."},
    ],
    "answer": "a",
    "explanation": "Unexpected attachments are a common malware delivery method. Always verify using trusted contact details before opening anything, and report suspicious messages appropriately.",
    "points": 10,
},
{
    "id": "mal_002",
    "domain": "malware",
    "title": "Fake Software Update Pop-up",
    "difficulty": "medium",
    "question": "While browsing a website, a pop-up says: 'Your computer is infected. Install this update now to stay protected.' It looks official and urgent. What is the best response?",
    "options": [
        {"id": "a", "text": "Install the update because security updates are important."},
        {"id": "b", "text": "Close the browser immediately, use company-approved security tools to scan the device, and report the incident if required."},
        {"id": "c", "text": "Restart the computer and continue working as normal."},
        {"id": "d", "text": "Search online to see if the message is legitimate before taking any action."},
    ],
    "answer": "b",
    "explanation": "Fake update pop-ups are designed to install malware. Close the browser, rely on approved security tools, and report the incident rather than interacting with the pop-up.",
    "points": 20,
},
{
    "id": "mal_003",
    "domain": "malware",
    "title": "USB Drop Attack",
    "difficulty": "hard",
    "question": "You find an unlabelled USB stick in the office car park. It could contain impportant information. What is the safest action?",
    "options": [
        {"id": "a", "text": "Leave it with reception or in a communal area so the owner can collect it."},
        {"id": "b", "text": "Plug it into a spare computer to identify the owner."},
        {"id": "c", "text": "Hand it in through the organisation’s approved process so it can be handled safely."},
        {"id": "d", "text": "Take it home and check it on your personal device."},
    ],
    "answer": "c",
    "explanation": "Unknown USB devices can contain malware designed to activate when plugged in. They should only be handled using approved organisational procedures.",
    "points": 30,
},
    # -------------------------
    # IMPERSONATION & DEEPFAKES (3)
    # -------------------------
    {
    "id": "imp_001",
    "domain": "impersonation",
    "title": "Teams Message From 'Your Manager'",
    "difficulty": "easy",
    "question": "You get a Teams message from someone with your manager’s name saying: 'I’m in a meeting — send me the latest staff contact list ASAP.' What should you do?",
    "options": [
        {"id": "a", "text": "Ask them to confirm using a trusted method (known phone number, in person, or verified Teams account) before sharing any information."},
        {"id": "b", "text": "Send the list but remove phone numbers and email addresses to reduce the risk."},
        {"id": "c", "text": "Ignore the message completely and continue working."},
        {"id": "d", "text": "Send the list quickly to avoid delaying your manager."},
    ],
    "answer": "a",
    "explanation": "Impersonation can occur via compromised or lookalike accounts. Always verify identity using trusted contact methods before sharing staff or personal data.",
    "points": 10,
},
{
    "id": "imp_002",
    "domain": "impersonation",
    "title": "Voice Call Urgency (Possible Deepfake)",
    "difficulty": "medium",
    "question": "You receive a phone call that sounds like a senior leader. They urgently ask you to reset a user password and read it out over the phone. What is the safest response?",
    "options": [
        {"id": "a", "text": "Reset the password but send it via a secure channel so the senior leader can access it safely."},
        {"id": "b", "text": "Follow official procedures: verify identity using trusted channels and never share passwords. Escalate through the approved process if needed."},
        {"id": "c", "text": "Refuse the request and hang up without reporting it."},
        {"id": "d", "text": "Comply because the voice sounds genuine and urgent."},
    ],
    "answer": "b",
    "explanation": "Impersonation and deepfake attacks rely on urgency and authority. Passwords should never be shared, and identity must be verified using approved, trusted channels.",
    "points": 20,
},
{
    "id": "imp_003",
    "domain": "impersonation",
    "title": "Lookalike Domain Email",
    "difficulty": "hard",
    "question": "You get an email from what looks like a trusted partner, but the email address is slightly different (e.g., .co instead of .com). The request seems like normal business. What should you do?",
    "options": [
        {"id": "a", "text": "Proceed as normal since the request looks legitimate."},
        {"id": "b", "text": "Verify the request using a trusted contact method you already have, not by replying to the email."},
        {"id": "c", "text": "Reply to the email asking them to confirm the request before taking any action."},
        {"id": "d", "text": "Forward the email to colleagues so they are aware."},
    ],
    "answer": "b",
    "explanation": "Lookalike domains are commonly used in impersonation attacks. Verification must be done using trusted contact details, not the email itself.",
    "points": 30,
},
    # -------------------------
    # DATA HANDLING & OVERSHARING (3)
    # -------------------------
    {
    "id": "data_001",
    "domain": "data_handling",
    "title": "Screenshot With Personal Data",
    "difficulty": "easy",
    "question": "You want quick help from a colleague, so you take a screenshot of your screen and send it. You later notice it includes a resident’s name, address and reference number. What should you do?",
    "options": [
        {"id": "a", "text": "Ask your colleague to delete it, report it using the company process, and avoid sharing personal data in screenshots in future."},
        {"id": "b", "text": "Do nothing — it was sent internally and will be forgotten."},
        {"id": "c", "text": "Message your colleague asking them to delete the screenshot and avoid using it, but don’t formally report it."},
        {"id": "d", "text": "Post a warning about it on social media so others don’t do it."},
    ],
    "answer": "a",
    "explanation": "Accidental sharing of personal data should be treated as an incident. Ask for deletion, report it promptly, and use safer methods (redaction/approved tools) next time.",
    "points": 10,
},
{
    "id": "data_002",
    "domain": "data_handling",
    "title": "Sending Work Files to Personal Email",
    "difficulty": "medium",
    "question": "You’re behind on work and want to finish at home. You consider emailing documents to your personal email account. What is the safest option?",
    "options": [
        {"id": "a", "text": "Email them to yourself temporarily so you can finish the work, then delete the files afterwards."},
        {"id": "b", "text": "Use approved remote access/tools (VPN/secure portal) or request the correct access rather than moving files to personal accounts."},
        {"id": "c", "text": "Upload them to a free file-sharing site so you can download them at home."},
        {"id": "d", "text": "Copy them to a USB stick and take it home."},
    ],
    "answer": "b",
    "explanation": "Moving work data to personal accounts or unapproved services increases breach risk and may break policy. Use approved remote access methods or request the proper access.",
    "points": 20,
},
{
    "id": "data_003",
    "domain": "data_handling",
    "title": "Minimum Data Principle",
    "difficulty": "hard",
    "question": "A colleague asks you to send them a full export of resident/customer data so they can 'filter it down' for a report. What is the best response?",
    "options": [
        {"id": "a", "text": "Send the full export — they can delete what they don’t need later."},
        {"id": "b", "text": "Challenge the need, share only the minimum necessary data, and use approved secure tools/processes for sharing."},
        {"id": "c", "text": "Send the full dataset but pseudonymise it (remove names) so it’s no longer personal data."},
        {"id": "d", "text": "Upload it to a shared drive and tell them where it is."},
    ],
    "answer": "b",
    "explanation": "The safest approach is data minimisation: only share what’s necessary, and only through approved secure methods. Over-sharing increases breach risk and can breach policy/law.",
    "points": 30,
},
    # -------------------------
    # DEVICES, REMOTE & PHYSICAL RISK (3)
    # -------------------------
    {
    "id": "dev_001",
    "domain": "devices",
    "title": "Laptop Left Unattended",
    "difficulty": "easy",
    "question": "You’re working in a public place and step away for a moment, leaving your work laptop on the table. What is the safest behaviour?",
    "options": [
        {"id": "a", "text": "Lock the screen and take the laptop with you (or secure it) before stepping away."},
        {"id": "b", "text": "Leave it — you’ll only be gone for 30 seconds."},
        {"id": "c", "text": "Ask a stranger nearby to watch it for you."},
        {"id": "d", "text": "Close the lid so the screen is hidden, then step away briefly."},
    ],
    "answer": "a",
    "explanation": "Unattended devices are a common cause of data loss or theft. Always lock your screen and keep the device with you or properly secured when stepping away.",
    "points": 10,
},
{
    "id": "dev_002",
    "domain": "devices",
    "title": "Public Wi-Fi and Remote Work",
    "difficulty": "medium",
    "question": "You need to access work systems while travelling. You’re on free public Wi-Fi. What’s the safest option?",
    "options": [
        {"id": "a", "text": "Use public Wi-Fi as long as the website shows HTTPS and looks legitimate."},
        {"id": "b", "text": "Email documents to your personal account so you can work offline."},
        {"id": "c", "text": "Use approved secure access (VPN/secure portal) or a trusted hotspot, and avoid sensitive work on open Wi-Fi."},
        {"id": "d", "text": "Turn off the firewall to improve connection speed."},
    ],
    "answer": "c",
    "explanation": "Public Wi-Fi can be monitored or spoofed. Approved secure access methods like VPNs or trusted hotspots reduce risk and align with remote-working policy.",
    "points": 20,
},
{
    "id": "dev_003",
    "domain": "devices",
    "title": "Shoulder Surfing + Screen Privacy",
    "difficulty": "hard",
    "question": "You’re working on sensitive information on a train and notice someone behind you can see your screen. What should you do?",
    "options": [
        {"id": "a", "text": "Keep working — it’s unlikely they’re paying attention."},
        {"id": "b", "text": "Turn the brightness up so you can finish more quickly."},
        {"id": "c", "text": "Take a quick photo of the screen so you can close the laptop and finish the work later in a private place."},
        {"id": "d", "text": "Angle the screen away, use a privacy filter if available, lock when not actively using, and avoid sensitive tasks in public where possible."},
    ],
    "answer": "d",
    "explanation": "Public environments increase the risk of visual data exposure. Reduce screen visibility, lock when not actively working, and avoid sensitive tasks in public spaces when possible.",
    "points": 30,
},
]

# In-memory progress store (prototype)
# PROGRESS[staff_id][scenario_id] = {"completed": True, "correct": bool, "selected_option": "a", "points_awarded": 10}
PROGRESS = {}


def _public_list_item(s):
    return {
        "id": s["id"],
        "domain": s["domain"],
        "title": s["title"],
        "difficulty": s["difficulty"],
    }


def _public_detail(s):
    return {
        "id": s["id"],
        "domain": s["domain"],
        "title": s["title"],
        "difficulty": s["difficulty"],
        "question": s["question"],
        "options": s["options"],
        "points": s["points"],
    }


@router.get("/scenarios")
def list_scenarios():
    return {"scenarios": [_public_list_item(s) for s in SCENARIOS]}


@router.get("/scenarios/{domain_id}")
def scenarios_by_domain(domain_id: str):
    return {"scenarios": [_public_list_item(s) for s in SCENARIOS if s["domain"] == domain_id]}


@router.get("/scenario/{scenario_id}")
def scenario_detail(scenario_id: str):
    for s in SCENARIOS:
        if s["id"] == scenario_id:
            return _public_detail(s)
    return {"error": "Scenario not found"}


# ✅ Accept both old + new frontend payloads to stop the 422 loop.
class SubmitPayload(BaseModel):
    staff_id: str
    scenario_id: str
    option_id: Optional[str] = None
    selected_option: Optional[str] = None


@router.post("/submit")
def submit_answer(payload: SubmitPayload):
    staff_id = (payload.staff_id or "").strip()
    scenario_id = (payload.scenario_id or "").strip()
    option_id = (payload.option_id or payload.selected_option or "").strip()

    if not staff_id:
        return {"error": "Missing staff_id"}
    if not scenario_id:
        return {"error": "Missing scenario_id"}
    if not option_id:
        return {"error": "Missing option_id"}

    scenario = None
    for s in SCENARIOS:
        if s["id"] == scenario_id:
            scenario = s
            break

    if scenario is None:
        return {"error": "Scenario not found"}

    # Ensure staff bucket exists
    if staff_id not in PROGRESS:
        PROGRESS[staff_id] = {}

    # ✅ First answer counts: do not allow overwriting a completed scenario
    existing = PROGRESS[staff_id].get(scenario_id)
    if existing and existing.get("completed"):
        return {
            "scenario_id": scenario_id,
            "already_attempted": True,
            "locked": True,
            "correct": bool(existing.get("correct")),
            "explanation": scenario["explanation"],
            # IMPORTANT: do not re-award points on re-submits
            "points_awarded": existing.get("points_awarded", 0),
            "progress": PROGRESS[staff_id],
        }

    # First attempt
    is_correct = option_id == scenario["answer"]
    points_awarded = scenario["points"] if is_correct else 0

    PROGRESS[staff_id][scenario_id] = {
        "completed": True,
        "correct": bool(is_correct),
        "selected_option": option_id,
        "points_awarded": int(points_awarded),
    }

    return {
        "scenario_id": scenario_id,
        "already_attempted": False,
        "locked": True,
        "correct": bool(is_correct),
        "explanation": scenario["explanation"],
        "points_awarded": int(points_awarded),
        "progress": PROGRESS[staff_id],
    }


@router.get("/progress/{staff_id}")
def get_progress(staff_id: str):
    staff_id = staff_id.strip()
    return {"staff_id": staff_id, "progress": PROGRESS.get(staff_id, {})}


def _calc_percent(correct: int, attempted: int) -> int:
    if attempted <= 0:
        return 0
    return int(round((correct / attempted) * 100))


@router.get("/completion/{staff_id}")
def completion_summary(staff_id: str):
    staff_id = staff_id.strip()
    staff_progress = PROGRESS.get(staff_id, {})

    scenarios_by_domain = {}
    for s in SCENARIOS:
        scenarios_by_domain.setdefault(s["domain"], []).append(s["id"])

    domain_results = []
    overall_attempted = 0
    overall_correct = 0

    for d in DOMAINS:
        domain_id = d["id"]
        scenario_ids = scenarios_by_domain.get(domain_id, [])

        attempted = 0
        correct = 0

        for sid in scenario_ids:
            entry = staff_progress.get(sid)
            if entry and entry.get("completed"):
                attempted += 1
                if entry.get("correct"):
                    correct += 1

        total = len(scenario_ids)
        score_percent = _calc_percent(correct, attempted)

        all_attempted = (total > 0) and (attempted == total)
        passed = all_attempted and (score_percent >= PASS_MARK_PERCENT)

        if total == 0:
            status = "no_scenarios"
        elif not all_attempted:
            status = "in_progress"
        else:
            status = "passed" if passed else "failed"

        overall_attempted += attempted
        overall_correct += correct

        domain_results.append(
            {
                "domain_id": domain_id,
                "domain_title": d["title"],
                "total_scenarios": total,
                "attempted": attempted,
                "correct": correct,
                "score_percent": score_percent,
                "pass_mark": PASS_MARK_PERCENT,
                "status": status,
                "complete": bool(passed),
            }
        )

    domains_with_scenarios = [dr for dr in domain_results if dr["total_scenarios"] > 0]
    training_complete = (
        all(dr["status"] == "passed" for dr in domains_with_scenarios)
        if domains_with_scenarios
        else False
    )
    overall_percent = _calc_percent(overall_correct, overall_attempted)

    return {
        "staff_id": staff_id,
        "overall": {
            "attempted": overall_attempted,
            "correct": overall_correct,
            "score_percent": overall_percent,
            "training_complete": training_complete,
            "pass_mark": PASS_MARK_PERCENT,
        },
        "domains": domain_results,
    }


# Admin reset endpoint (exists in your handover list)
class ResetPayload(BaseModel):
    staff_id: Optional[str] = None


@router.post("/admin/reset")
def admin_reset(payload: Optional[ResetPayload] = None):
    # If staff_id provided: reset that user only, else reset all
    if payload and payload.staff_id:
        sid = payload.staff_id.strip()
        PROGRESS[sid] = {}
        return {"ok": True, "reset": "staff", "staff_id": sid}
    for key in PROGRESS:
     PROGRESS[key] = {}
    return {"ok": True, "reset": "all"}
