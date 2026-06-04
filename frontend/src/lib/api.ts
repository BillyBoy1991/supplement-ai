const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, token?: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new ApiError(res.status, body.detail ?? "Request failed");
  }
  return res.json() as Promise<T>;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface QuestionOption {
  label: string;
  value: string;
}

export type QuestionType = "number" | "single_choice" | "multi_choice" | "text";

export interface Question {
  id: string;
  prompt: string;
  type: QuestionType;
  options?: QuestionOption[];
}

export interface StepResponse {
  session_id: string;
  finished: boolean;
  question: Question | null;
}

export interface Recommendation {
  slug: string;
  name: string;
  category: string;
  evidence_level: string;
  standard_dose: string;
  mechanisms: string[];
  score: number;
  score_breakdown: Record<string, unknown>;
  safety_flags: string[];
}

export interface RecommendationsResponse {
  session_id: string;
  need_scores: Record<string, number>;
  disclaimer: string;
  disclaimer_version: number;
  advisory: string | null;
  recommendations: Recommendation[];
}

export const auth = {
  register: (email: string, password: string) =>
    request<TokenResponse>("/auth/register", undefined, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  login: (email: string, password: string) =>
    request<TokenResponse>("/auth/login", undefined, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
};

export const questionnaire = {
  start: (token: string) => request<StepResponse>("/questionnaire/start", token, { method: "POST" }),

  answer: (token: string, sessionId: string, answer: unknown) =>
    request<StepResponse>("/questionnaire/answer", token, {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, answer }),
    }),
};

export const recommendations = {
  get: (token: string, sessionId: string) =>
    request<RecommendationsResponse>(`/recommendations/${sessionId}`, token),
};
