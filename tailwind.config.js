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
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            ul: {
              "--tw-prose-bullets": theme("colors.sky[300]"),
              "list-style": "disc",
              ".dark &": {
                "--tw-prose-bullets": theme("colors.indigo[800]"),
              },
            },
            a: {
              color: "inherit",
              "text-decoration-color": theme("colors.sky[400]"),
              "font-weight": "inherit",
              ".dark &": {
                "text-decoration-color": theme("colors.indigo[400]"),
              },
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
