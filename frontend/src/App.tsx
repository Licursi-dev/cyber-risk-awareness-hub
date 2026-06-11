import React, { useEffect, useMemo, useState } from "react";
import {
  apiGetDomains,
  apiGetScenariosByDomain,
  apiGetScenario,
  apiSubmitAnswer,
  apiGetCompletion,
  apiAdminResetProgress,
  type Domain,
  type ScenarioListItem,
  type ScenarioDetail,
} from "./api";

type View =
  | { name: "start" }
  | { name: "home" }
  | { name: "domain"; domainId: string; domainTitle: string }
  | { name: "scenario"; scenarioId: string; domainId: string; domainTitle: string }
  | { name: "summary" }
  | { name: "admin" };

export default function App() {
  const [staffId, setStaffId] = useState<string>(() => {

    return localStorage.getItem("staff_id") || "Guest";
  
  });
  const [view, setView] = useState<View>(() =>
    localStorage.getItem("staff_id") ? { name: "home" } : { name: "start" }
  );

  const [domains, setDomains] = useState<Domain[]>([]);
  const [loadingDomains, setLoadingDomains] = useState(false);
  const [domainsError, setDomainsError] = useState<string>("");

  const [completion, setCompletion] = useState<any>(null);
  const [loadingCompletion, setLoadingCompletion] = useState(false);
  const [completionError, setCompletionError] = useState<string>("");

  const [scenarios, setScenarios] = useState<ScenarioListItem[]>([]);
  const [loadingScenarios, setLoadingScenarios] = useState(false);
  const [scenariosError, setScenariosError] = useState<string>("");

  const [scenario, setScenario] = useState<ScenarioDetail | null>(null);
  const [loadingScenario, setLoadingScenario] = useState(false);
  const [scenarioError, setScenarioError] = useState<string>("");

  const [selectedOption, setSelectedOption] = useState<string>("");
  const [submitResult, setSubmitResult] = useState<{
    correct: boolean;
    points_awarded: number;
    explanation?: string;
    already_attempted?: boolean;
  } | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string>("");

  // Admin
  const [adminPin, setAdminPin] = useState("");
  const [adminTargetStaffId, setAdminTargetStaffId] = useState("");
  const [adminStatus, setAdminStatus] = useState<string>("");
  const [adminWorking, setAdminWorking] = useState(false);

  const hasStaffId = useMemo(() => staffId.trim().length > 0, [staffId]);

  // --------- Helpers to make UI work even if backend response shape changes ---------

  const derivedOverall = useMemo(() => {
    const domainsArr: any[] = completion?.domains ?? [];
    const totalScenarios = domainsArr.reduce((sum, d) => sum + (Number(d?.total_scenarios) || 0), 0);
    const attempted =
      Number(completion?.overall?.attempted) ||
      domainsArr.reduce((sum, d) => sum + (Number(d?.attempted) || 0), 0);

    const attemptedPercent =
      totalScenarios > 0 ? Math.round((attempted / totalScenarios) * 100) : 0;

    const domainsWithScenarios = domainsArr.filter((d) => (Number(d?.total_scenarios) || 0) > 0).length;
    const domainsPassed = domainsArr.filter((d) => d?.status === "passed").length;

    const scorePercent = Number(completion?.overall?.score_percent) || 0;
    const passMark = Number(completion?.overall?.pass_mark) || 70;
    const trainingComplete = Boolean(completion?.overall?.training_complete);

    const correct =
      Number(completion?.overall?.correct) ||
      domainsArr.reduce((sum, d) => sum + (Number(d?.correct) || 0), 0);

    return {
      totalScenarios,
      attempted,
      attemptedPercent,
      domainsWithScenarios,
      domainsPassed,
      scorePercent,
      passMark,
      trainingComplete,
      correct,
    };
  }, [completion]);

  // Load domains once
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setLoadingDomains(true);
        setDomainsError("");
        const d = await apiGetDomains();
        if (!cancelled) setDomains(d);
      } catch (e: any) {
        if (!cancelled) setDomainsError(e?.message || "Failed to load domains");
      } finally {
        if (!cancelled) setLoadingDomains(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  async function refreshCompletion() {
    if (!staffId) return;
    try {
      setLoadingCompletion(true);
      setCompletionError("");
      const c = await apiGetCompletion(staffId);
      setCompletion(c);
    } catch (e: any) {
      setCompletionError(e?.message || "Failed to load progress");
    } finally {
      setLoadingCompletion(false);
    }
  }

  // Refresh completion whenever staffId changes
  useEffect(() => {
    if (hasStaffId) refreshCompletion();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasStaffId]);

  async function openDomain(domainId: string, domainTitle: string) {
    setView({ name: "domain", domainId, domainTitle });
    setScenarios([]);
    setScenario(null);
    setSubmitResult(null);
    setSelectedOption("");
    setSubmitError("");

    try {
      setLoadingScenarios(true);
      setScenariosError("");
      const s = await apiGetScenariosByDomain(domainId);
      setScenarios(s);
    } catch (e: any) {
      setScenariosError(e?.message || "Failed to load scenarios");
    } finally {
      setLoadingScenarios(false);
    }
  }

  async function openScenario(domainId: string, domainTitle: string, scenarioId: string) {
    setView({ name: "scenario", scenarioId, domainId, domainTitle });
    setScenario(null);
    setSubmitResult(null);
    setSelectedOption("");
    setSubmitError("");

    try {
      setLoadingScenario(true);
      setScenarioError("");
      const d = await apiGetScenario(scenarioId);
      setScenario(d);
    } catch (e: any) {
      setScenarioError(e?.message || "Failed to load scenario");
    } finally {
      setLoadingScenario(false);
    }
  }

  async function submitAnswer() {
    if (!staffId || !scenario?.id || !selectedOption) return;

    try {
      setSubmitting(true);
      setSubmitError("");

      const res = await apiSubmitAnswer({
        staff_id: staffId,
        scenario_id: scenario.id,
        selected_option: selectedOption,
      });

      setSubmitResult(res);
      await refreshCompletion();
    } catch (e: any) {
      setSubmitError(e?.message || "Submit failed");
    } finally {
      setSubmitting(false);
    }
  }

  function changeStaff() {
    localStorage.removeItem("staff_id");
    setStaffId("");
    setCompletion(null);
    setView({ name: "start" });
  }

  async function setStaffAndContinue() {

    const cleaned = staffId.trim();
  
    if (!cleaned) return;
  
    localStorage.setItem("staff_id", cleaned);
  
    setStaffId(cleaned);
  
    setView({ name: "home" });
  
    try {
  
      setLoadingCompletion(true);
  
      setCompletionError("");
  
      const c = await apiGetCompletion(cleaned);
  
      setCompletion(c);
  
    } catch (e: any) {
  
      setCompletionError(e?.message || "Failed to load progress");
  
    } finally {
  
      setLoadingCompletion(false);
  
    }
  
  }

  async function doAdminReset() {
    setAdminStatus("");
    if (!adminPin.trim()) {
      setAdminStatus("Enter PIN.");
      return;
    }
    if (!adminTargetStaffId.trim()) {
      setAdminStatus("Enter staff ID to reset.");
      return;
    }

    try {
      setAdminWorking(true);
      const res = await apiAdminResetProgress({
        pin: adminPin.trim(),
        staff_id: adminTargetStaffId.trim(),
      });

      if (res?.error) setAdminStatus(`Error: ${res.error}`);
      else if (res?.detail) setAdminStatus(`Error: ${res.detail}`);
      else setAdminStatus(res?.message || "Reset complete.");

      await refreshCompletion();
    } catch (e: any) {
      setAdminStatus(e?.message || "Admin reset failed.");
    } finally {
      setAdminWorking(false);
    }
  }

  // ----- UI -----

  const cardStyle: React.CSSProperties = {
    border: "1px solid rgba(255,255,255,0.25)",
    borderRadius: 14,
    padding: 14,
    background: "rgba(0,0,0,0.15)",
    textAlign: "center",
    boxShadow: "0 0 0 1px rgba(120,90,255,0.25), 0 0 40px rgba(120,90,255,0.15)",
  };

  const btnStyle: React.CSSProperties = {
    padding: "10px 14px",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.15)",
    background: "rgba(0,0,0,0.35)",
    color: "white",
    opacity: 0.95,
    cursor: "pointer",
    transition: "all 0.15s ease",
    fontSize: 16,
  };

  const smallBtnStyle: React.CSSProperties = {
    ...btnStyle,
    padding: "8px 12px",
    fontSize: 14,
    opacity: 0.85,
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        paddingBottom: 100,
        background: "url('/bg.png') center / cover no-repeat, radial-gradient(900px 520px at 18% 12%, rgba(120, 90, 255, 0.28), transparent 60%), radial-gradient(720px 480px at 82% 18%, rgba(0, 200, 255, 0.16), transparent 55%), radial-gradient(900px 620px at 50% 92%, rgba(130, 80, 255, 0.16), transparent 60%), #0b0d14",
        color: "white",
        padding: 24,
        maxWidth: 1100,
        margin: "0 auto",
        fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",
      }}
    >
      <h1 style={{ fontSize: 56, margin: "0 0 12px 0", letterSpacing: -1, textAlign: "center" }}>
        Cyber Risk & Awareness Hub
      </h1>

      {view.name !== "start" && (
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 12, marginBottom: 16 }}>
          <div style={{ opacity: 0.8 }}>
          <span style={{ opacity: 0.6, fontSize: 14 }}>Staff ID</span>: <b>{staffId}</b>
          </div>
          <button style={smallBtnStyle} onClick={changeStaff}>
          ✏️ Edit
          </button>
          <button style={smallBtnStyle} onClick={() => setView({ name: "admin" })}>
           ⚙️ Admin
          </button>
        </div>
      )}

      {view.name === "start" && (
        <div style={{ maxWidth: 900 }}>
          <h2 style={{ fontSize: 40, marginTop: 10 }}>Start</h2>
          <p style={{ opacity: 0.75, fontSize: 18 }}>
            Enter your staff ID to begin. This links your progress to you (server-side).
          </p>

          <input
            value={staffId}
            onChange={(e) => setStaffId(e.target.value)}
            placeholder="e.g. JSMITH or 10482"
            style={{
              width: "100%",
              maxWidth: 620,
              padding: 14,
              borderRadius: 12,
              border: "1px solid rgba(255,255,255,0.2)",
              background: "rgba(0,0,0,0.25)",
              color: "white",
              fontSize: 18,
            }}
          />

          <div style={{ marginTop: 12 }}>
          <button className="crah-btn" style={btnStyle} onClick={setStaffAndContinue} disabled={!staffId.trim()}>
              Continue
            </button>
          </div>

          <p style={{ marginTop: 18, opacity: 0.6 }}>
            Note: This is a prototype. In production, staff ID would come from a login (Microsoft/Entra ID).
          </p>
        </div>
      )}

      {view.name === "home" && (
        <div style={{ maxWidth: 980, margin: "0 auto" }}>
          <div style={{ ...cardStyle, marginBottom: 16, maxWidth: 760, margin: "0 auto" }}>
          <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 8, textAlign: "center" }}>Training status</div>

            {loadingCompletion ? (
              <div style={{ opacity: 0.8 }}>Loading...</div>
            ) : completionError ? (
              <div style={{ color: "#ff6b6b" }}>{completionError}</div>
            ) : completion ? (
              <>
                <div style={{ opacity: 0.9 }}>
                  Training progress: <b>{derivedOverall.attemptedPercent}%</b> (
                  {derivedOverall.attempted}/{derivedOverall.totalScenarios} scenarios attempted)
                </div>
                <div style={{ opacity: 0.8, marginTop: 6 }}>
                  Domains passed: <b>{derivedOverall.domainsPassed}</b>/
                  {derivedOverall.domainsWithScenarios} • Overall score:{" "}
                  <b>{derivedOverall.scorePercent}%</b> (pass mark{" "}
                  {derivedOverall.passMark}%) • Training complete:{" "}
                  <b>{derivedOverall.trainingComplete ? "Yes" : "No"}</b>
                </div>
              </>
            ) : (
              <div style={{ opacity: 0.8 }}>No data yet</div>
            )}

           <div style={{ display: "flex", gap: 10, marginTop: 12, justifyContent: "center" }}>
              <button style={smallBtnStyle} onClick={() => setView({ name: "summary" })}>
                View summary
              </button>
              <button style={smallBtnStyle} onClick={refreshCompletion}>
                Refresh
              </button>
            </div>
          </div>

          <h2 style={{ fontSize: 34, margin: "10px 0 10px", textAlign: "center" }}>Choose a topic</h2>

          {loadingDomains ? (
            <div style={{ opacity: 0.8 }}>Loading domains...</div>
          ) : domainsError ? (
            <div style={{ color: "#ff6b6b" }}>{domainsError}</div>
          ) : (
            <ul style={{ listStyle: "disc", paddingLeft: 22, margin: "0 auto", maxWidth: 600 }}>
              {domains.map((d) => {
                const domainRow = completion?.domains?.find((x: any) => x.domain_id === d.id);
                const statusText =
                  domainRow?.status === "no_scenarios"
                    ? "No scenarios"
                    : domainRow?.attempted === domainRow?.total_scenarios && (domainRow?.total_scenarios ?? 0) > 0
                    ? `Passed (${domainRow?.attempted ?? 0}/${domainRow?.total_scenarios ?? 0})`
                    : `In progress (${domainRow?.attempted ?? 0}/${domainRow?.total_scenarios ?? 0})`;

                    const statusIcon =
                    domainRow?.attempted === domainRow?.total_scenarios && domainRow?.total_scenarios > 0
                      ? "✅"
                      : domainRow?.status === "no_scenarios"
                      ? "⚪"
                      : "🟡";            
                return (
                  <li key={d.id} style={{ marginBottom: 10, display: "flex", alignItems: "center", gap: 12, justifyContent: "center" }}>
                    <button style={btnStyle} onClick={() => openDomain(d.id, d.title)}>
                      {d.title}
                    </button>
                    <span style={{ opacity: 0.85 }}>
                      {statusIcon} {statusText}
                    </span>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}

      {view.name === "domain" && (
        <div style={{ maxWidth: 980 }}>
          <button style={smallBtnStyle} onClick={() => setView({ name: "home" })}>
            ← Back
          </button>

          <h2 style={{ fontSize: 38, marginTop: 14 }}>{view.domainTitle}</h2>

          <div style={{ ...cardStyle, marginBottom: 14 }}>
            {completion?.domains?.find((x: any) => x.domain_id === view.domainId)?.status === "passed" ? (
              <>
                <div style={{ fontWeight: 700 }}>✅ This domain is passed.</div>
                <div style={{ opacity: 0.75, marginTop: 6 }}>
                  You can still read scenarios to learn, but answering may be locked.
                </div>
              </>
            ) : (
              <div style={{ opacity: 0.85 }}>
                Complete all scenarios then hit the pass mark to pass this domain.
              </div>
            )}
          </div>

          {loadingScenarios ? (
            <div style={{ opacity: 0.8 }}>Loading scenarios...</div>
          ) : scenariosError ? (
            <div style={{ color: "#ff6b6b" }}>{scenariosError}</div>
          ) : scenarios.length === 0 ? (
            <div style={{ opacity: 0.75 }}>No scenarios yet.</div>
          ) : (
            <ul style={{ listStyle: "none", paddingLeft: 0, margin: "0 auto", maxWidth: 600, textAlign: "center" }}>
              {scenarios.map((s) => (
                <li key={s.id} style={{ marginBottom: 10 }}>
                  <button style={btnStyle} onClick={() => openScenario(view.domainId, view.domainTitle, s.id)}>
                    {s.title} — {s.difficulty}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {view.name === "scenario" && (
        <div style={{ maxWidth: 980 }}>
          <button style={smallBtnStyle} onClick={() => openDomain(view.domainId, view.domainTitle)}>
            ← Back to scenarios
          </button>

          {loadingScenario ? (
            <div style={{ opacity: 0.8, marginTop: 12 }}>Loading scenario...</div>
          ) : scenarioError ? (
            <div style={{ color: "#ff6b6b", marginTop: 12 }}>{scenarioError}</div>
          ) : !scenario ? null : (
            <>
              <h2 style={{ fontSize: 40, marginTop: 14 }}>{scenario.title}</h2>
              <div style={{ opacity: 0.8, marginBottom: 12 }}>
                Difficulty: {scenario.difficulty} • Points available: {scenario.points ?? 0}
              </div>

              <div style={{ fontSize: 20, fontWeight: 650, marginBottom: 10 }}>{scenario.question}</div>

              <div style={{ ...cardStyle, marginBottom: 12 }}>
                {(scenario.options ?? []).map((o) => (
                  <label key={o.id} style={{ display: "block", padding: "8px 0", cursor: "pointer" }}>
                    <input
                      type="radio"
                      name="opt"
                      value={o.id}
                      checked={selectedOption === o.id}
                      onChange={() => setSelectedOption(o.id)}
                      style={{ marginRight: 10 }}
                    />
                    {o.text}
                  </label>
                ))}
              </div>

              <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                <button style={btnStyle} onClick={submitAnswer} disabled={!selectedOption || submitting}>
                  {submitting ? "Submitting..." : "Submit answer"}
                </button>
                <button style={smallBtnStyle} onClick={refreshCompletion}>
                  Refresh progress
                </button>
              </div>

              {submitError && <div style={{ color: "#ff6b6b", marginTop: 10 }}>{submitError}</div>}

              {submitResult && (
                <div style={{ marginTop: 14 }}>
                  <div style={{ fontSize: 18 }}>
                  <b>Result:</b> {submitResult?.already_attempted ? "Already attempted (locked)" : submitResult?.correct ? "Correct" : "Incorrect"}
                  </div>
                  <div style={{ fontSize: 18 }}>
                    <b>Points awarded:</b> {submitResult.points_awarded}
                  </div>
                  {submitResult.explanation && (
                    <div style={{ marginTop: 10, opacity: 0.9 }}>
                      <b>Explanation:</b> {submitResult.explanation}
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      )}

      {view.name === "summary" && (
        <div style={{ maxWidth: 980 }}>
          <button style={smallBtnStyle} onClick={() => setView({ name: "home" })}>
            ← Back
          </button>

          <h2 style={{ fontSize: 38, marginTop: 14 }}>Your Summary</h2>

          {loadingCompletion ? (
            <div style={{ opacity: 0.8 }}>Loading...</div>
          ) : completionError ? (
            <div style={{ color: "#ff6b6b" }}>{completionError}</div>
          ) : !completion ? (
            <div style={{ opacity: 0.8 }}>No data yet</div>
          ) : (
            <>
              <div style={{ ...cardStyle, marginBottom: 14 }}>
                <div style={{ fontSize: 18, opacity: 0.9 }}>
                  Attempted: <b>{derivedOverall.attempted}</b> / {derivedOverall.totalScenarios}
                </div>
                <div style={{ fontSize: 18, opacity: 0.9, marginTop: 6 }}>
                  Correct: <b>{derivedOverall.correct}</b>
                </div>
                <div style={{ fontSize: 18, opacity: 0.9, marginTop: 6 }}>
                  Overall score: <b>{derivedOverall.scorePercent}%</b> (pass mark {derivedOverall.passMark}%)
                </div>
                <div style={{ fontSize: 18, opacity: 0.9, marginTop: 6 }}>
                  Training complete: <b>{derivedOverall.trainingComplete ? "Yes" : "No"}</b>
                </div>
              </div>

              <div style={{ ...cardStyle }}>
                <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 10 }}>Domain breakdown</div>
                <ul style={{ listStyle: "disc", paddingLeft: 22, margin: 0 }}>
                  {(completion?.domains ?? []).map((d: any) => (
                    <li key={d.domain_id} style={{ marginBottom: 10 }}>
                      <b>{d.domain_title}</b> — {d.status} — {d.attempted}/{d.total_scenarios} attempted — score{" "}
                      {d.score_percent}% (pass {d.pass_mark}%)
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>
      )}

      {view.name === "admin" && (
        <div style={{ maxWidth: 980 }}>
          <button style={smallBtnStyle} onClick={() => setView({ name: "home" })}>
            ← Back
          </button>

          <h2 style={{ fontSize: 38, marginTop: 14 }}>Admin — Reset Progress</h2>

          <div style={{ ...cardStyle, maxWidth: 720 }}>
            <div style={{ opacity: 0.85, marginBottom: 12 }}>
              This is a prototype admin tool. In production, this would be behind proper admin login (not a simple PIN). **hint** 1234 admin 
            </div>

            <div style={{ display: "grid", gap: 12 }}>
              <div>
                <div style={{ opacity: 0.85, marginBottom: 6 }}>Admin PIN</div>
                <input
                  value={adminPin}
                  onChange={(e) => setAdminPin(e.target.value)}
                  placeholder="Enter PIN"
                  type="password"
                  style={{
                    width: "100%",
                    padding: 12,
                    borderRadius: 12,
                    border: "1px solid rgba(255,255,255,0.2)",
                    background: "rgba(0,0,0,0.25)",
                    color: "white",
                    fontSize: 16,
                  }}
                />
              </div>

              <div>
                <div style={{ opacity: 0.85, marginBottom: 6 }}>Staff ID to reset</div>
                <input
                  value={adminTargetStaffId}
                  onChange={(e) => setAdminTargetStaffId(e.target.value)}
                  placeholder="e.g. admin"
                  style={{
                    width: "100%",
                    padding: 12,
                    borderRadius: 12,
                    border: "1px solid rgba(255,255,255,0.2)",
                    background: "rgba(0,0,0,0.25)",
                    color: "white",
                    fontSize: 16,
                  }}
                />
              </div>

              <div style={{ display: "flex", gap: 10 }}>
                <button style={btnStyle} onClick={doAdminReset} disabled={adminWorking}>
                  {adminWorking ? "Working..." : "Reset progress"}
                </button>
                <button
                  style={smallBtnStyle}
                  onClick={() => {
                    setAdminPin("");
                    setAdminTargetStaffId("");
                    setAdminStatus("");
                  }}
                >
                  Clear
                </button>
              </div>

              {adminStatus && <div style={{ marginTop: 6, opacity: 0.95 }}>{adminStatus}</div>}
              </div>
          </div>
        </div>
      )}

      {/* Fixed signature - SOLID background to prevent clash */}
      <div
        style={{
          position: "fixed",
          bottom: 20,
          left: "50%",
          transform: "translateX(-50%)",
          background: "#0b0d14",
          border: "1px solid rgba(0,255,255,0.35)",
          borderRadius: 8,
          padding: "8px 18px",
          textAlign: "center",
          letterSpacing: "1px",
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            fontSize: 10,
            opacity: 0.65,
            marginBottom: 2
          }}
        >
          Powered by
        </div>

        <div
          style={{
            fontSize: 14,
            fontWeight: 600,
            letterSpacing: 1.5
          }}
        >
          licursi.dev
        </div>
      </div>

    </div>
  );
}
