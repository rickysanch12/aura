/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0f9ff",
          500: "#0ea5e9",
          900: "#0c4a6e",
        },
        dark: {
          50: "#f9fafb",
          100: "#f3f4f6",
          900: "#111827",
          950: "#030712",
        },
      },
      animation: {
        glow: "glow 2s ease-in-out infinite",
        pulse: "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        glow: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
    },
  },
  plugins: [],
  darkMode: "class",
};
