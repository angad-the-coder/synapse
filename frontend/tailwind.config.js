const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  darkMode: "class",
  content: [
    "components/**/*.vue",
    "layouts/**/*.vue",
    "pages/**/*.vue",
    "composables/**/*.{js,ts}",
    "plugins/**/*.{js,ts}",
    "App.{js,ts,vue}",
    "app.{js,ts,vue}",
  ],
  theme: {
    fontFamily: {
      sans: ["Manrope", ...defaultTheme.fontFamily.sans],
    },
    extend: {
      fontSize: {
        xxs: ["0.625rem", "0.75rem"],
      },
      keyframes: {
        expand: {
          '0%': { width: '0%' },
          '100%': { width: '100%' },
        },
      },
      animation: {
        expand: 'expand 14.5s linear infinite',
      },
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            ul: {
              "--tw-prose-bullets": theme("colors.amber[300]"),
              "list-style": "disc",
            },
            a: {
              color: "inherit",
              "text-decoration-color": theme("colors.amber[400]"),
              "font-weight": "inherit",
              "text-decoration-thickness": "1px",
              "&:hover": {
                "text-decoration-thickness": "2px",
              },
            },
          },
        },
      }),
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@headlessui/tailwindcss"),
    require("@tailwindcss/typography"),
  ],
};
