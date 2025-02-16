<template>
  <div class="max-w-7xl mx-auto h-56 w-full p-4">
    <div class="flex w-full space-x-2">
      <StyledDiv class="w-full grow">
        <template #title>
          Brainwave Stream
        </template>
      </StyledDiv>
      <StyledDiv center class="max-w-96 w-full shrink-0">
        <template #title>
          Stress Levels
        </template>
        <div class="space-y-4 py-4">
          <PercentCircle :percent="sample == null ? 0 : sample.level / 100" class="h-36 w-36">
            <div class="flex space-x-0.5 items-end">
              <div v-if="sample == null" class="bg-gray-300 animate-pulse h-4 mb-1.5 w-6 rounded-md" />
              <h2 v-else class="text-2xl font-semibold text-gray-800 tabular-nums">{{ sample.level }}</h2>
              <h3 class="text-lg text-gray-500">/ 100</h3>
            </div>
          </PercentCircle>
          <div class="flex flex-col items-center">
            <p class="text-sm tracking-wide uppercase font-medium text-gray-400 mb-1">
              Updates in <span class="tabular-nums">{{ secToUpdate }}</span> SEC
            </p>
            <div class="w-36 rounded-b rounded-t-sm h-1 bg-gray-100 overflow-hidden">
              <div class="bg-gray-300 h-full transition-[width] duration-2000" :class="startAnimation ? 'animate-expand' : 'w-0'" />
            </div>
          </div>
        </div>
      </StyledDiv>
    </div>
    <StyledDiv>
      <template #title>
        Generated Prompt
      </template>
    </StyledDiv>
    <StyledDiv>
      <template #title>
        Generated Images
      </template>
    </StyledDiv>
  </div>
</template>
<script setup lang="ts">
// Using existing Terra information from last night, simulate real-time 
// data stream as proof of concept (updates every 15 seconds)
const { data } = await useFetch("/api/terra/stress", {
  query: {
    start_date: "2025-02-15"
  }
})

const sampleIdx = ref(-1);
const secToUpdate = ref(15);
const startAnimation = ref(false);
const sample = computed(() => sampleIdx.value < 0 ? null : data.value.samples[sampleIdx.value]);

onMounted(() => {
  sampleIdx.value = (data.value!.samples as IStressSample[]).findIndex(
    (sample) => sample.timestamp === "2025-02-15T22:50:00.000000-07:55"
  )
  secToUpdate.value = 15;
  setTimeout(() => startAnimation.value = true, 500)
  setInterval(() => {
    if (secToUpdate.value === 1) {
      sampleIdx.value++;
      secToUpdate.value = 15;
      startAnimation.value = false;
      setTimeout(() => startAnimation.value = true, 500)
    } else {
      secToUpdate.value = secToUpdate.value - 1;
    }
  }, 1000);
})

</script>
