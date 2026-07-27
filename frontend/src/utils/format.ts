export function stringList(value: unknown): string[] {
  if (Array.isArray(value)) return value.filter((item): item is string => typeof item === "string" && item.trim().length > 0);
  if (typeof value === "string" && value.trim()) return [value];
  return [];
}

export function joinedList(value: unknown, fallback = "Unknown"): string {
  const items = stringList(value);
  return items.length ? items.join(", ") : fallback;
}
