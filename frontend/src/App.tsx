import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { AlertCircle, ArrowRight, Shield } from "lucide-react";
import { v4 as uuidv4 } from "uuid";

import { Sidebar } from "./components/sidebar/Sidebar";
import { ChatInput } from "./components/chat/ChatInput";
import { LoadingState } from "./components/chat/LoadingState";
import { AssistantResponse } from "./components/chat/AssistantResponse";
import { sendChat } from "./services/chat";
import type { ChatMessage } from "./types/chat";

const suggestions = ["Show Apache HTTP Server vulnerabilities", "List critical VMware CVEs", "Which vulnerabilities are known to be exploited?", "Show RCE vulnerabilities published after 2023", "Find CVEs affecting Microsoft Exchange", "Show vulnerabilities requiring immediate action"];
export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]); const [loading, setLoading] = useState(false); const [error, setError] = useState<string | null>(null); const [lastQuery, setLastQuery] = useState(""); const [collapsed, setCollapsed] = useState(false); const bottom = useRef<HTMLDivElement>(null);
  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading, error]);
  const ask = async (query: string) => { setError(null); setLastQuery(query); setMessages(old => [...old, { id: uuidv4(), role: "user", content: query }]); setLoading(true); try { const response = await sendChat(query); setMessages(old => [...old, { id: uuidv4(), role: "assistant", response }]); } catch (e) { setError(e instanceof Error ? e.message : "Unable to connect to the cybersecurity assistant."); } finally { setLoading(false); } };
  const fresh = () => { setMessages([]); setError(null); setLastQuery(""); };
  const welcome = messages.length === 0;
  return <div className="flex h-screen overflow-hidden bg-[radial-gradient(ellipse_at_top,_#14213b_0%,_#0B1220_46%)]"><Sidebar collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} onNewChat={fresh} />
    <main className="flex min-w-0 flex-1 flex-col"><header className="flex h-16 shrink-0 items-center border-b border-border px-5 md:px-8"><div className="flex items-center gap-2 text-sm font-medium"><Shield className="h-4 w-4 text-blue-400 md:hidden" />Cybersecurity workspace</div></header>
      <div className="scrollbar-thin flex-1 overflow-y-auto"><div className={welcome ? "mx-auto flex min-h-full max-w-5xl flex-col justify-center px-5 py-10" : "mx-auto max-w-5xl px-5 py-8"}>{welcome ? <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="mx-auto w-full max-w-3xl text-center"><div className="mx-auto mb-6 grid h-14 w-14 place-items-center rounded-2xl border border-blue-400/20 bg-blue-500/10 text-blue-300"><Shield className="h-7 w-7" /></div><h1 className="text-3xl font-semibold tracking-tight md:text-4xl">Cybersecurity Vulnerability Assistant</h1><p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-slate-400 md:text-base">Ask questions about CVEs, vendors, products, attack vectors, severity, ransomware usage, CISA KEV vulnerabilities, and mitigation recommendations.</p><div className="mt-8"><ChatInput onSubmit={ask} disabled={loading} /></div><div className="mt-5 grid gap-2 text-left sm:grid-cols-2">{suggestions.map(s => <button key={s} onClick={() => ask(s)} className="group flex items-center justify-between rounded-xl border border-border bg-card/70 px-4 py-3 text-sm text-slate-300 transition hover:border-slate-600 hover:bg-slate-800"><span>{s}</span><ArrowRight className="h-4 w-4 shrink-0 text-slate-600 transition group-hover:translate-x-0.5 group-hover:text-blue-400" /></button>)}</div></motion.div> : <div className="space-y-7">{messages.map(message => message.role === "user" ? <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} key={message.id} className="ml-auto max-w-[85%] rounded-2xl rounded-tr-sm bg-blue-600 px-4 py-3 text-sm shadow-lg shadow-blue-950/20">{message.content}</motion.div> : message.response && <AssistantResponse key={message.id} response={message.response} />)}{loading && <LoadingState />}{error && <div className="max-w-lg rounded-xl border border-red-500/25 bg-red-500/[.07] p-4"><div className="flex gap-2 text-sm font-medium text-red-200"><AlertCircle className="h-4 w-4 shrink-0" />Could not generate a response</div><p className="mt-1 text-sm text-red-200/70">{error}</p><button onClick={() => ask(lastQuery)} className="mt-3 rounded-lg bg-red-500/15 px-3 py-1.5 text-xs font-semibold text-red-200 hover:bg-red-500/25">Retry request</button></div>}<div ref={bottom} /></div>}</div></div>
      {!welcome && <div className="border-t border-border bg-background/80 px-5 py-4 backdrop-blur"><div className="mx-auto max-w-4xl"><ChatInput onSubmit={ask} disabled={loading} /><p className="mt-2 text-center text-[11px] text-slate-600">Responses are generated from available vulnerability intelligence. Verify findings before taking action.</p></div></div>}
    </main></div>;
}
