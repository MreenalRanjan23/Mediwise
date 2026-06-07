const API_BASE = "http://127.0.0.1:8000";

export async function analyzeMedicationPlan(data: any) {

  const response = await fetch(
    `${API_BASE}/clinical/analyze`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {

    throw new Error(
      "Failed to analyze medication plan"
    );
  }

  return response.json();
}