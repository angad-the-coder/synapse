<template>
  <div class="max-w-7xl mx-auto w-full p-4">
    <div class="prose mx-auto">
      <h1>
        Setup
      </h1>
      <p>
        Before you can use the demo, you must complete the setup process by connecting to the Terra API below.
      </p>
      <div class="not-prose" :class="pending && 'animate-pulse opacity-50'">
        <div v-if="pending" class=" bg-sky-300 px-3 py-4 rounded inline-block">
          <div class="bg-white/50 h-2 rounded w-24" />
        </div>
        <NuxtLink v-else-if="loginData.status === 'success'" :to="loginData.url" class="rounded bg-sky-500 text-white hover:bg-sky-600 px-3 py-2">
          Authenticate with Terra
        </NuxtLink>
        <div v-else class="rounded border-2 border-gray-200">
          Something went wrong :/ Try again later.
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
const { data: loginData, pending } = await useLazyFetch("/api/terra");
</script>
