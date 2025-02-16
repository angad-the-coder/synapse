<template>
  <div class="mx-auto flex h-full max-w-7xl py-12 flex-col space-y-12 items-center">
    <div class="rounded-lg border-2 w-[65ch] border-gray-100 overflow-hidden bg-gradient-to-tr from-gray-100 to-white flex items-center justify-center py-16">
      <Logo class="h-40" />
    </div>
    <div class="prose">
      <h1>
        About
      </h1>
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam earum tempora minima perferendis expedita distinctio officiis architecto laudantium quibusdam porro.
      </p>
    </div>
  </div>
</template>
<style>
.electrode-section {
    display: flex;
    flex-wrap: wrap;
    padding: 5px;
}

.electrode-item {
    margin: 5px;
}

.electrode-item h3 {
    text-align: center;
    margin-bottom: 4px;
}

canvas {
    background: #333;
    border: solid black 1px;
}
</style>
<script setup lang="ts">

// import { channelNames, type EEGReading, MuseClient } from "muse-js";

// (window as any).connect = async () => {
//     const graphTitles = Array.from(document.querySelectorAll('.electrode-item h3'));
//     const canvases = Array.from(document.querySelectorAll('.electrode-item canvas')) as HTMLCanvasElement[];
//     const canvasCtx = canvases.map((canvas) => canvas.getContext('2d'));

//     graphTitles.forEach((item, index) => {
//         item.textContent = channelNames[index];
//     });

//     function plot(reading: EEGReading) {
//         const canvas = canvases[reading.electrode];
//         const context = canvasCtx[reading.electrode];
//         if (!context) {
//             return;
//         }
//         const width = canvas.width / 12.0;
//         const height = canvas.height / 2.0;
//         context.fillStyle = 'green';
//         context.clearRect(0, 0, canvas.width, canvas.height);

//         for (let i = 0; i < reading.samples.length; i++) {
//             const sample = reading.samples[i] / 15.;
//             if (sample > 0) {
//                 context.fillRect(i * 25, height - sample, width, sample);
//             } else {
//                 context.fillRect(i * 25, height, width, -sample);
//             }
//         }
//     }

//     const client = new MuseClient();
//     client.connectionStatus.subscribe((status) => {
//         console.log(status ? 'Connected!' : 'Disconnected');
//     });

//     try {
//         client.enableAux = true;
//         await client.connect();
//         await client.start();
//         document.getElementById('headset-name')!.innerText = client.deviceName;
//         client.eegReadings.subscribe((reading) => {
//             plot(reading);
//         });
//         client.telemetryData.subscribe((reading) => {
//             document.getElementById('temperature')!.innerText = reading.temperature.toString() + '℃';
//             document.getElementById('batteryLevel')!.innerText = reading.batteryLevel.toFixed(2) + '%';
//         });
//         client.accelerometerData.subscribe((accel) => {
//             const normalize = (v: number) => (v / 16384.).toFixed(2) + 'g';
//             document.getElementById('accelerometer-x')!.innerText = normalize(accel.samples[2].x);
//             document.getElementById('accelerometer-y')!.innerText = normalize(accel.samples[2].y);
//             document.getElementById('accelerometer-z')!.innerText = normalize(accel.samples[2].z);
//         });
//         await client.deviceInfo().then((deviceInfo) => {
//             document.getElementById('hardware-version')!.innerText = deviceInfo.hw;
//             document.getElementById('firmware-version')!.innerText = deviceInfo.fw;
//         });
//     } catch (err) {
//         console.error('Connection failed', err);
//     }
// };

</script>
