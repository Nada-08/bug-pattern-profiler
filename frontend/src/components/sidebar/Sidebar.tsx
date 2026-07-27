import { motion } from "framer-motion";
import { ChevronLeft, Plus, ShieldCheck } from "lucide-react";
import { cn } from "../../utils/cn";

export function Sidebar({ collapsed, onToggle, onNewChat }: { collapsed: boolean; onToggle: () => void; onNewChat: () => void }) {
  return <motion.aside animate={{ width: collapsed ? 76 : 272 }} className="relative hidden shrink-0 flex-col border-r border-border bg-[#0d1524] p-3 md:flex">
    <button onClick={onToggle} className="absolute -right-3 top-6 z-10 rounded-full border border-border bg-card p-1.5 text-slate-400 hover:text-white"><ChevronLeft className={cn("h-4 w-4 transition-transform", collapsed && "rotate-180")} /></button>
    <div className="flex h-12 items-center gap-3 px-2"><div className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-blue-600 shadow-lg shadow-blue-950/40"><ShieldCheck className="h-5 w-5" /></div>{!collapsed && <span className="font-semibold tracking-tight">CyberRAG <span className="text-blue-400">Assistant</span></span>}</div>
    <button onClick={onNewChat} className="mt-6 flex h-11 items-center justify-center gap-2 rounded-xl bg-blue-600 text-sm font-medium shadow-lg shadow-blue-950/30 transition hover:bg-blue-500"><Plus className="h-4 w-4" />{!collapsed && "New chat"}</button>
  </motion.aside>;
}
