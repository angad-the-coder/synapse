<template>
  <div class="fixed z-50 h-12 w-full border-b border-gray-300/50 bg-gray-50 px-4 opacity-100 sm:h-16 sm:shadow overflow-hidden">
    <div class="mx-auto flex h-full max-w-7xl items-center justify-between">
      <NuxtLink to="/">
        <Logo class="h-7 sm:h-8 w-auto" />
      </NuxtLink>
      <div class="flex items-center space-x-2">
        <div class="flex items-center space-x-3 sm:space-x-4">
          <NuxtLink class="text-sm font-medium text-gray-500 hover:text-amber-600" to="/about">
            About
          </NuxtLink>
          <NuxtLink class="text-sm font-medium text-gray-500 hover:text-amber-600" to="/demo">
            Demo
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
defineProps<{
  showPageLinks?: boolean;
}>();
</script>
