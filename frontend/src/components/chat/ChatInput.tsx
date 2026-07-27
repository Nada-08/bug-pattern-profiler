import { FormEvent, useState } from "react";
import { ArrowUp, LoaderCircle } from "lucide-react";

export function ChatInput({ onSubmit, disabled, initialValue = "" }: { onSubmit: (query: string) => void; disabled?: boolean; initialValue?: string }) {
  const [value, setValue] = useState(initialValue);
  const submit = (event: FormEvent) => { event.preventDefault(); if (value.trim() && !disabled) { onSubmit(value.trim()); setValue(""); } };
  return <form onSubmit={submit} className="relative rounded-2xl border border-slate-700/80 bg-card p-2 shadow-card transition focus-within:border-slate-500">
    <input value={value} onChange={(event) => setValue(event.target.value)} placeholder="Ask about vulnerabilities, vendors, CVEs..." className="h-11 w-full bg-transparent px-3 pr-12 text-sm outline-none placeholder:text-slate-500" />
    <button disabled={!value.trim() || disabled} aria-label="Send message" className="absolute right-3 top-3 grid h-9 w-9 place-items-center rounded-xl bg-blue-600 text-white transition hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500">{disabled ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <ArrowUp className="h-5 w-5" />}</button>
  </form>;
}
