/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Noto Sans KR"', '"Inter"', 'system-ui', 'sans-serif'],
        display: ['"Inter"', '"Noto Sans KR"', 'system-ui', 'sans-serif'],
        mono: ['"SF Mono"', '"Fira Code"', 'monospace'],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive) / <alpha-value>)",
          foreground: "hsl(var(--destructive-foreground) / <alpha-value>)",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
        gold: "#C9A96E",
        cream: "#FCF9F5",
        beige: "#F5F0E6",
        wood: "#3D2B1F",
        oak: "#8B5E3C",
      },
      borderRadius: {
        xl: "calc(var(--radius) + 4px)",
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xs: "calc(var(--radius) - 6px)",
      },
      boxShadow: {
        xs: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        editorial: "0 8px 32px rgb(0 0 0 / 0.08)",
        "editorial-lg": "0 16px 48px rgb(0 0 0 / 0.12)",
      },
      letterSpacing: {
        widest: "0.15em",
        display: "-0.02em",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "caret-blink": {
          "0%,70%,100%": { opacity: "1" },
          "20%,50%": { opacity: "0" },
        },
        "fade-up": {
          from: { opacity: "0", transform: "translateY(30px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "pulse-line": {
          "0%, 100%": { opacity: "0.3", transform: "scaleY(0.6)" },
          "50%": { opacity: "1", transform: "scaleY(1)" },
        },
        "draw-line": {
          from: { strokeDashoffset: "1000" },
          to: { strokeDashoffset: "0" },
        },
        "sunray-1": {
          "0%, 100%": { opacity: "0.18", transform: "translate(0%, 0%) scale(1)" },
          "30%":      { opacity: "0.28", transform: "translate(3%, -4%) scale(1.08)" },
          "60%":      { opacity: "0.20", transform: "translate(-2%, 3%) scale(0.96)" },
        },
        "sunray-2": {
          "0%, 100%": { opacity: "0.10", transform: "translate(0%, 0%) scale(1)" },
          "40%":      { opacity: "0.18", transform: "translate(-4%, 5%) scale(1.12)" },
          "70%":      { opacity: "0.12", transform: "translate(2%, -2%) scale(0.94)" },
        },
        "sunray-3": {
          "0%, 100%": { opacity: "0.08", transform: "translate(0%, 0%) scale(1)" },
          "50%":      { opacity: "0.16", transform: "translate(5%, 2%) scale(1.06)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "caret-blink": "caret-blink 1.25s ease-out infinite",
        "fade-up": "fade-up 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards",
        "fade-in": "fade-in 0.6s ease forwards",
        "pulse-line": "pulse-line 2s ease-in-out infinite",
        "draw-line": "draw-line 1.5s ease forwards",
        "sunray-1": "sunray-1 9s  ease-in-out infinite",
        "sunray-2": "sunray-2 13s ease-in-out infinite",
        "sunray-3": "sunray-3 17s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}