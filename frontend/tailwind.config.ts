import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#030816",
        panel: "#0a1122",
        primary: {
          DEFAULT: "#62d4ff",
          shimmer: "#7a7cff",
          glow: "rgba(98, 212, 255, 0.45)"
        },
        secondary: "#db2777",
        muted: "#94a3b8",
        border: "rgba(255, 255, 255, 0.1)"
      },
      boxShadow: {
        panel: "0 25px 70px rgba(0, 0, 0, 0.4)",
        glow: "0 0 20px rgba(98, 212, 255, 0.25)"
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
        "3xl": "2rem"
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in": "fadeIn 0.5s ease-out forwards"
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        }
      }
    }
  },
  plugins: []
};

export default config;
