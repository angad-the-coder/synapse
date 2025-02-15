module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:vue/essential",
    "plugin:@typescript-eslint/recommended",
    "plugin:tailwindcss/recommended",
    "@nuxtjs/eslint-config-typescript",
  ],
  parserOptions: {
    ecmaVersion: "latest",
    parser: "@typescript-eslint/parser",
    sourceType: "module",
  },
  plugins: ["vue", "tailwindcss", "@typescript-eslint"],
  rules: {
    quotes: ["error", "double"],
    semi: ["error", "always"],
    indent: ["error", 2],
    "no-multi-spaces": ["error"],
    "comma-dangle": ["error", "always-multiline"],
    "space-before-function-paren": [
      "error",
      {
        anonymous: "always",
        named: "never",
        asyncArrow: "always",
      },
    ],
    // for nuxt pages:
    camelcase: "off",
    "tailwindcss/no-custom-classname": "off",
    "vue/multi-word-component-names": "off",
    // for transition component:
    "vue/attribute-hyphenation": "off",
    "vue/no-custom-modifiers-on-v-model": "off",
    "vue/no-v-for-template-key": "off",
    // for tailwind config:
    "@typescript-eslint/no-var-requires": "off",
    "no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
  },
  settings: {
    tailwindcss: {
      cssFiles: [
        "components/**/*.vue",
        "layouts/**/*.vue",
        "pages/**/*.vue",
        "composables/**/*.{js,ts}",
        "plugins/**/*.{js,ts}",
        "App.{js,ts,vue}",
        "app.{js,ts,vue}",
        "!**/node_modules",
        "!**/.nuxt",
      ],
    },
  },
};
