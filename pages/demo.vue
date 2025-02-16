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
        Generated Video
      </template>
    </StyledDiv>
  </div>
</template>
<script setup lang="ts">
// const { data } = await useFetch("/api/terra/stress", {
//   query: {
//     start_date: "2025-02-15"
//   }
// })

const data = {
  value: {
    samples: [
      { "timestamp": "2025-02-15T22:47:00.000000-07:55", "level": 39 }, { "timestamp": "2025-02-15T22:50:00.000000-07:55", "level": 41 }, { "timestamp": "2025-02-15T22:53:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T22:56:00.000000-07:55", "level": 40 }, { "timestamp": "2025-02-15T22:59:00.000000-07:55", "level": 37 }, { "timestamp": "2025-02-15T23:02:00.000000-07:55", "level": 41 }, { "timestamp": "2025-02-15T23:05:00.000000-07:55", "level": 29 }, { "timestamp": "2025-02-15T23:08:00.000000-07:55", "level": 54 }, { "timestamp": "2025-02-15T23:11:00.000000-07:55", "level": 34 }, { "timestamp": "2025-02-15T23:14:00.000000-07:55", "level": 47 }, { "timestamp": "2025-02-15T23:17:00.000000-07:55", "level": 49 }, { "timestamp": "2025-02-15T23:20:00.000000-07:55", "level": 41 }, { "timestamp": "2025-02-15T23:23:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T23:26:00.000000-07:55", "level": 37 }, { "timestamp": "2025-02-15T23:29:00.000000-07:55", "level": 34 }, { "timestamp": "2025-02-15T23:32:00.000000-07:55", "level": 34 }, { "timestamp": "2025-02-15T23:35:00.000000-07:55", "level": 52 }, { "timestamp": "2025-02-15T23:38:00.000000-07:55", "level": 52 }, { "timestamp": "2025-02-15T23:41:00.000000-07:55", "level": 41 }, { "timestamp": "2025-02-15T23:44:00.000000-07:55", "level": 55 }, { "timestamp": "2025-02-15T23:47:00.000000-07:55", "level": 61 }, { "timestamp": "2025-02-15T23:50:00.000000-07:55", "level": 51 } ], "body_battery_samples": [ { "timestamp": "2025-02-15T10:38:00.000000-07:55", "level": 61 }, { "timestamp": "2025-02-15T10:41:00.000000-07:55", "level": 61 }, { "timestamp": "2025-02-15T10:44:00.000000-07:55", "level": 61 }, { "timestamp": "2025-02-15T10:47:00.000000-07:55", "level": 60 }, { "timestamp": "2025-02-15T10:50:00.000000-07:55", "level": 60 }, { "timestamp": "2025-02-15T10:53:00.000000-07:55", "level": 60 }, { "timestamp": "2025-02-15T10:56:00.000000-07:55", "level": 60 }, { "timestamp": "2025-02-15T10:59:00.000000-07:55", "level": 59 }, { "timestamp": "2025-02-15T11:02:00.000000-07:55", "level": 59 }, { "timestamp": "2025-02-15T11:05:00.000000-07:55", "level": 59 }, { "timestamp": "2025-02-15T11:08:00.000000-07:55", "level": 58 }, { "timestamp": "2025-02-15T11:11:00.000000-07:55", "level": 58 }, { "timestamp": "2025-02-15T11:14:00.000000-07:55", "level": 58 }, { "timestamp": "2025-02-15T11:17:00.000000-07:55", "level": 57 }, { "timestamp": "2025-02-15T11:20:00.000000-07:55", "level": 57 }, { "timestamp": "2025-02-15T11:23:00.000000-07:55", "level": 57 }, { "timestamp": "2025-02-15T11:26:00.000000-07:55", "level": 57 }, { "timestamp": "2025-02-15T11:29:00.000000-07:55", "level": 57 }, { "timestamp": "2025-02-15T11:32:00.000000-07:55", "level": 56 }, { "timestamp": "2025-02-15T11:35:00.000000-07:55", "level": 56 }, { "timestamp": "2025-02-15T11:38:00.000000-07:55", "level": 56 }, { "timestamp": "2025-02-15T11:41:00.000000-07:55", "level": 56 }, { "timestamp": "2025-02-15T11:44:00.000000-07:55", "level": 55 }, { "timestamp": "2025-02-15T11:47:00.000000-07:55", "level": 55 }, { "timestamp": "2025-02-15T11:50:00.000000-07:55", "level": 55 }, { "timestamp": "2025-02-15T11:53:00.000000-07:55", "level": 55 }, { "timestamp": "2025-02-15T11:56:00.000000-07:55", "level": 55 }, { "timestamp": "2025-02-15T11:59:00.000000-07:55", "level": 54 }, { "timestamp": "2025-02-15T12:02:00.000000-07:55", "level": 54 }, { "timestamp": "2025-02-15T12:05:00.000000-07:55", "level": 54 }, { "timestamp": "2025-02-15T12:08:00.000000-07:55", "level": 54 }, { "timestamp": "2025-02-15T12:11:00.000000-07:55", "level": 54 }, { "timestamp": "2025-02-15T12:14:00.000000-07:55", "level": 53 }, { "timestamp": "2025-02-15T12:17:00.000000-07:55", "level": 53 }, { "timestamp": "2025-02-15T12:20:00.000000-07:55", "level": 53 }, { "timestamp": "2025-02-15T12:23:00.000000-07:55", "level": 53 }, { "timestamp": "2025-02-15T12:26:00.000000-07:55", "level": 53 }, { "timestamp": "2025-02-15T12:29:00.000000-07:55", "level": 52 }, { "timestamp": "2025-02-15T12:32:00.000000-07:55", "level": 52 }, { "timestamp": "2025-02-15T12:35:00.000000-07:55", "level": 52 }, { "timestamp": "2025-02-15T12:38:00.000000-07:55", "level": 52 }, { "timestamp": "2025-02-15T12:41:00.000000-07:55", "level": 51 }, { "timestamp": "2025-02-15T12:44:00.000000-07:55", "level": 51 }, { "timestamp": "2025-02-15T12:47:00.000000-07:55", "level": 51 }, { "timestamp": "2025-02-15T12:50:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T12:53:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T12:56:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T12:59:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T13:02:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T13:05:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T13:08:00.000000-07:55", "level": 50 }, { "timestamp": "2025-02-15T13:11:00.000000-07:55", "level": 49 }, { "timestamp": "2025-02-15T13:14:00.000000-07:55", "level": 49 }, { "timestamp": "2025-02-15T13:17:00.000000-07:55", "level": 49 }, { "timestamp": "2025-02-15T13:20:00.000000-07:55", "level": 48 }, { "timestamp": "2025-02-15T13:23:00.000000-07:55", "level": 48 }, { "timestamp": "2025-02-15T13:26:00.000000-07:55", "level": 48 }, { "timestamp": "2025-02-15T13:29:00.000000-07:55", "level": 47 }, { "timestamp": "2025-02-15T13:32:00.000000-07:55", "level": 47 }, { "timestamp": "2025-02-15T13:35:00.000000-07:55", "level": 47 }, { "timestamp": "2025-02-15T13:38:00.000000-07:55", "level": 47 }, { "timestamp": "2025-02-15T13:41:00.000000-07:55", "level": 47 }, { "timestamp": "2025-02-15T13:44:00.000000-07:55", "level": 47 }, { "timestamp": "2025-02-15T13:47:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T13:50:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T13:53:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T13:56:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T13:59:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T14:11:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T14:14:00.000000-07:55", "level": 46 }, { "timestamp": "2025-02-15T14:17:00.000000-07:55", "level": 45 }, { "timestamp": "2025-02-15T14:20:00.000000-07:55", "level": 45 }, { "timestamp": "2025-02-15T14:47:00.000000-07:55", "level": 44 }, { "timestamp": "2025-02-15T14:50:00.000000-07:55", "level": 44 }, { "timestamp": "2025-02-15T14:53:00.000000-07:55", "level": 43 }, { "timestamp": "2025-02-15T14:56:00.000000-07:55", "level": 43 }, { "timestamp": "2025-02-15T14:59:00.000000-07:55", "level": 43 }, { "timestamp": "2025-02-15T15:02:00.000000-07:55", "level": 43 }, { "timestamp": "2025-02-15T15:05:00.000000-07:55", "level": 43 }, { "timestamp": "2025-02-15T15:08:00.000000-07:55", "level": 43 }, { "timestamp": "2025-02-15T16:20:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:23:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:26:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:29:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:32:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:35:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:38:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:41:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:44:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:47:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:50:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:53:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:56:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T16:59:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T17:02:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T17:05:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T17:08:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T17:11:00.000000-07:55", "level": 38 }, { "timestamp": "2025-02-15T17:14:00.000000-07:55", "level": 37 }, { "timestamp": "2025-02-15T17:17:00.000000-07:55", "level": 37 }, { "timestamp": "2025-02-15T17:20:00.000000-07:55", "level": 37 }, { "timestamp": "2025-02-15T17:23:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:26:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:29:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:32:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:35:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:38:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:41:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:44:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:47:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:50:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:53:00.000000-07:55", "level": 36 }, { "timestamp": "2025-02-15T17:56:00.000000-07:55", "level": 35 }, { "timestamp": "2025-02-15T17:59:00.000000-07:55", "level": 35 }, { "timestamp": "2025-02-15T18:02:00.000000-07:55", "level": 35 }, { "timestamp": "2025-02-15T18:05:00.000000-07:55", "level": 34 }, { "timestamp": "2025-02-15T18:08:00.000000-07:55", "level": 34 }, { "timestamp": "2025-02-15T18:11:00.000000-07:55", "level": 34 }, { "timestamp": "2025-02-15T18:14:00.000000-07:55", "level": 34 }, { "timestamp": "2025-02-15T20:14:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T20:17:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T20:20:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T22:08:00.000000-07:55", "level": 24 }, { "timestamp": "2025-02-15T22:47:00.000000-07:55", "level": 30 }, { "timestamp": "2025-02-15T22:50:00.000000-07:55", "level": 30 }, { "timestamp": "2025-02-15T22:53:00.000000-07:55", "level": 30 }, { "timestamp": "2025-02-15T22:56:00.000000-07:55", "level": 30 }, { "timestamp": "2025-02-15T22:59:00.000000-07:55", "level": 30 }, { "timestamp": "2025-02-15T23:02:00.000000-07:55", "level": 30 }, { "timestamp": "2025-02-15T23:05:00.000000-07:55", "level": 30 }, { "timestamp": "2025-02-15T23:08:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:11:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:14:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:17:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:20:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:23:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:26:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:29:00.000000-07:55", "level": 28 }, { "timestamp": "2025-02-15T23:32:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T23:35:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T23:38:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T23:41:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T23:44:00.000000-07:55", "level": 27 }, { "timestamp": "2025-02-15T23:47:00.000000-07:55", "level": 26 }, { "timestamp": "2025-02-15T23:50:00.000000-07:55", "level": 26 }
    ]
  }
}

// Using existing Terra information from last night, simulate real-time 
// data stream as proof of concept (updates every 15 seconds)

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
