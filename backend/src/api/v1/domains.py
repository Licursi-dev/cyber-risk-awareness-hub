from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["domains"])

DOMAINS = [
    {"id": "passwords", "title": "Passwords & Authentication"},
    {"id": "phishing", "title": "Phishing & Social Engineering"},
    {"id": "credential_theft", "title": "Credential Theft"},
    {"id": "bec", "title": "Business Email Compromise"},
    {"id": "malware", "title": "Malware & Ransomware"},
    {"id": "impersonation", "title": "Impersonation & Deepfakes"},
    {"id": "data_handling", "title": "Data Handling & Oversharing"},
    {"id": "devices", "title": "Devices, Remote & Physical Risk"},
]

@router.get("/domains")
def list_domains():
    return {"domains": DOMAINS}
@router.get("/domains/{domain_id}")
def get_domain(domain_id: str):
    for d in DOMAINS:
        if d["id"] == domain_id:
            return d
    return {"error": "Domain not found"}