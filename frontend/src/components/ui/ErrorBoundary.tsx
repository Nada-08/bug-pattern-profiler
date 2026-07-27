import { Component, type ErrorInfo, type ReactNode } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface Props { children: ReactNode; }
interface State { hasError: boolean; }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };
  static getDerivedStateFromError(): State { return { hasError: true }; }
  componentDidCatch(error: Error, info: ErrorInfo) { console.error("CyberRAG UI render error", error, info); }
  render() {
    if (!this.state.hasError) return this.props.children;
    return <main className="grid min-h-screen place-items-center bg-background px-5 text-slate-100"><div className="max-w-md rounded-2xl border border-red-500/25 bg-card p-6 text-center shadow-card"><AlertTriangle className="mx-auto h-7 w-7 text-red-300" /><h1 className="mt-3 font-semibold">Something went wrong</h1><p className="mt-2 text-sm leading-6 text-slate-400">The assistant interface encountered an unexpected error. Refresh to start a new session.</p><button onClick={() => window.location.reload()} className="mx-auto mt-5 flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-500"><RefreshCw className="h-4 w-4" />Refresh app</button></div></main>;
  }
}
