export interface Source { cve_id?: string; title?: string; vendor: string[]; product: string[]; severity?: string; cvss_score?: number; score: number; source_type?: string; published_at?: string; required_action?: string; patch_status?: string; days_overdue?: number; }
export interface RankedCve extends Partial<Source> { cve_id?: string; id?: string; impact?: string; attacker_requirements?: string; priority_reason?: string; priority?: string; }
export interface ChatAnswer { query_summary?: string; priority_ranked_cves?: RankedCve[]; overdue_patches?: unknown[]; cross_cve_patterns?: string; recommended_actions?: string[]; hallucination_flags?: string[]; sources_used?: unknown[]; }
export interface ChatResponse { answer: ChatAnswer; sources: Source[]; }
export interface ChatMessage { id: string; role: "user" | "assistant"; content?: string; response?: ChatResponse; }
