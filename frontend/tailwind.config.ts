import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";
export default {
  darkMode: ["class"], content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: { colors: { background: "#0B1220", card: "#111827", border: "#1F2937", primary: "#2563EB" }, boxShadow: { card: "0 12px 30px rgb(0 0 0 / .16)" } } },
  plugins: [animate],
} satisfies Config;
