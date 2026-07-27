import type { ChatResponse } from "../types/chat";

export async function sendChat(query: string): Promise<ChatResponse> {
  const response = await fetch("/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query }) });
  if (!response.ok) throw new Error(`The server returned ${response.status}.`);
  return response.json() as Promise<ChatResponse>;
}
