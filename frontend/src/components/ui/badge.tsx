import { type ReactNode } from "react";
import { cn } from "../../utils/cn";
export function Badge({ children, tone = "slate" }: { children: ReactNode; tone?: "slate" | "blue" | "green" | "amber" | "red" }) {
  const tones = { slate: "bg-slate-800 text-slate-300", blue: "bg-blue-500/15 text-blue-300", green: "bg-emerald-500/15 text-emerald-300", amber: "bg-amber-500/15 text-amber-300", red: "bg-red-500/15 text-red-300" };
  return <span className={cn("inline-flex items-center rounded-md px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide", tones[tone])}>{children}</span>;
}
