const API_BASE = "https://f10em1lsbbmhmrm3gjy8yp0y.178.104.40.223.sslip.io";

export type Domain = { id: string; title: string };

export type ScenarioListItem = {
  id: string;
  domain: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
};

export type ScenarioDetail = ScenarioListItem & {
  question?: string;
  options?: { id: string; text: string }[];
  answer?: string; // backend may not send this, but OK if it does
  explanation?: string;
  points?: number;
};

export type SubmitAnswerResponse = {

  correct: boolean;

  points_awarded: number;

  explanation?: string;

  already_attempted?: boolean;

};

/** Small helper: safe JSON parse */
async function readJsonSafe(r: Response): Promise<any> {
  try {
    return await r.json();
  } catch {
    return null;
  }
}

/**
 * IMPORTANT:
 * Different versions of your backend/frontend have used slightly different keys.
 * This function makes the submit response "stable" for App.tsx:
 *   - always returns { correct, points_awarded, explanation }
 *   - points_awarded defaults to 0 if missing
 */
function normaliseSubmitResponse(data: any): SubmitAnswerResponse {
  // correct can appear as: correct / is_correct
  const correctRaw = data?.correct ?? data?.is_correct ?? false;
  const correct = Boolean(correctRaw);

  // points can appear as: points_awarded / pointsAwarded / points / score / awarded
  const pointsRaw =
    data?.points_awarded ??
    data?.pointsAwarded ??
    data?.points ??
    data?.score ??
    data?.awarded ??
    0;

  // Ensure number + default 0
  const points_awarded =
    typeof pointsRaw === "number"
      ? pointsRaw
      : typeof pointsRaw === "string"
      ? Number(pointsRaw) || 0
      : 0;

  // explanation can appear as: explanation / detail / message
  const explanation = data?.explanation ?? data?.detail ?? data?.message ?? undefined;

return {

  correct,

  points_awarded,

  explanation,

  already_attempted: Boolean(data?.already_attempted),

};
}

export async function apiGetDomains(): Promise<Domain[]> {
  const r = await fetch(`${API_BASE}/api/v1/domains`);
  if (!r.ok) throw new Error("Failed to load domains");
  const data = await readJsonSafe(r);
  return data?.domains ?? [];
}

export async function apiGetScenariosByDomain(domainId: string): Promise<ScenarioListItem[]> {
  const r = await fetch(`${API_BASE}/api/v1/scenarios/${encodeURIComponent(domainId)}`);
  if (!r.ok) throw new Error("Failed to load domain scenarios");
  const data = await readJsonSafe(r);
  return data?.scenarios ?? [];
}

export async function apiGetScenario(scenarioId: string): Promise<ScenarioDetail> {
  const r = await fetch(`${API_BASE}/api/v1/scenario/${encodeURIComponent(scenarioId)}`);
  if (!r.ok) throw new Error("Failed to load scenario");
  const data = await readJsonSafe(r);
  return (data ?? {}) as ScenarioDetail;
}

/**
 * IMPORTANT:
 * Backend expects: { staff_id, scenario_id, option_id }
 * Frontend UI uses "selected_option" internally.
 * So we accept selected_option here but POST as option_id.
 */
export async function apiSubmitAnswer(payload: {
  staff_id: string;
  scenario_id: string;
  selected_option: string;
}): Promise<SubmitAnswerResponse> {
  const r = await fetch(`${API_BASE}/api/v1/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      staff_id: payload.staff_id,
      scenario_id: payload.scenario_id,
      option_id: payload.selected_option, // ✅ backend expects option_id
    }),
  });

  // If not ok, try to show backend error message
  if (!r.ok) {
    const data = await readJsonSafe(r);
    const fallbackText = await r.text().catch(() => "");
    const msg =
      data?.detail?.[0]?.msg ||
      data?.error ||
      data?.message ||
      fallbackText ||
      "Submit failed";
    throw new Error(msg);
  }

  const data = await readJsonSafe(r);
  return normaliseSubmitResponse(data);
}

export async function apiGetCompletion(staffId: string): Promise<any> {
  const r = await fetch(`${API_BASE}/api/v1/completion/${encodeURIComponent(staffId)}`);
  if (!r.ok) throw new Error("Failed to load completion");
  return await readJsonSafe(r);
}

export async function apiAdminResetProgress(payload: {
  pin: string;
  staff_id: string;
}): Promise<{ status?: string; message?: string; error?: string; detail?: string }> {
  const r = await fetch(`${API_BASE}/api/v1/admin/reset`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-admin-pin": payload.pin,
    },
    body: JSON.stringify({ staff_id: payload.staff_id }),
  });

  const data = await readJsonSafe(r);
  return data ?? {};
}
