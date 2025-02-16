// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/tailwindcss",
    "nuxt-headlessui",
    // "ngrok",
  ],
  // ngrok: {
  //   authtoken_from_env: true, // Use NGROK_AUTHTOKEN environment variable
  //   auth: 'username:password',
  //   domain: 'your_custom_domain',
  //   production: true,
  // }
  vite: {
    server: {
      allowedHosts: ["bf26-68-65-164-17.ngrok-free.app"] // Add your Ngrok domain here
    }
  }
})
