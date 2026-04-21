<template>
  <Transition name="slide">
    <div
      v-if="system.isVisible"
      class="w-80 shrink-0 bg-zinc-900 border-l border-zinc-800 flex flex-col overflow-hidden"
    >
      <!-- Header -->
      <div class="flex items-center justify-between px-4 py-3 border-b border-zinc-800">
        <h2 class="text-white font-semibold text-sm">System Monitor</h2>
        <button @click="system.toggle()" class="text-zinc-500 hover:text-white transition-colors text-lg">
          ✕
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-4 space-y-4">

        <!-- CPU -->
        <div v-if="system.cpu" class="bg-zinc-800 rounded-xl p-4">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs text-zinc-400 font-medium uppercase tracking-wider">CPU</span>
            <span class="text-white font-bold text-sm">{{ system.cpu.usage_percent }}%</span>
          </div>
          <div class="w-full bg-zinc-700 rounded-full h-1.5 mb-3">
            <div
              class="h-1.5 rounded-full transition-all duration-500"
              :class="barColor(system.cpu.usage_percent)"
              :style="{ width: system.cpu.usage_percent + '%' }"
            />
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs text-zinc-500">
            <div>Cores: <span class="text-zinc-300">{{ system.cpu.core_count }}</span></div>
            <div>Threads: <span class="text-zinc-300">{{ system.cpu.thread_count }}</span></div>
            <div class="col-span-2">Freq: <span class="text-zinc-300">{{ system.cpu.frequency_mhz }} MHz</span></div>
          </div>
        </div>

        <!-- RAM -->
        <div v-if="system.ram" class="bg-zinc-800 rounded-xl p-4">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs text-zinc-400 font-medium uppercase tracking-wider">RAM</span>
            <span class="text-white font-bold text-sm">{{ system.ram.usage_percent }}%</span>
          </div>
          <div class="w-full bg-zinc-700 rounded-full h-1.5 mb-3">
            <div
              class="h-1.5 rounded-full transition-all duration-500"
              :class="barColor(system.ram.usage_percent)"
              :style="{ width: system.ram.usage_percent + '%' }"
            />
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs text-zinc-500">
            <div>Used: <span class="text-zinc-300">{{ system.ram.used_gb }} GB</span></div>
            <div>Total: <span class="text-zinc-300">{{ system.ram.total_gb }} GB</span></div>
            <div class="col-span-2">Free: <span class="text-zinc-300">{{ system.ram.available_gb }} GB</span></div>
          </div>
        </div>

        <!-- GPU -->
        <div v-if="system.gpu.length > 0" v-for="g in system.gpu" :key="g.id" class="bg-zinc-800 rounded-xl p-4">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs text-zinc-400 font-medium uppercase tracking-wider">GPU</span>
            <span class="text-white font-bold text-sm">{{ g.load_percent }}%</span>
          </div>
          <div class="w-full bg-zinc-700 rounded-full h-1.5 mb-3">
            <div
              class="h-1.5 rounded-full transition-all duration-500"
              :class="barColor(g.load_percent)"
              :style="{ width: g.load_percent + '%' }"
            />
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs text-zinc-500">
            <div class="col-span-2 truncate">{{ g.name }}</div>
            <div>VRAM: <span class="text-zinc-300">{{ g.memory_used_mb }}MB / {{ g.memory_total_mb }}MB</span></div>
            <div>Temp: <span :class="g.temperature_c > 80 ? 'text-red-400' : 'text-zinc-300'">{{ g.temperature_c }}°C</span></div>
          </div>
        </div>

        <!-- Top Processes -->
        <div class="bg-zinc-800 rounded-xl p-4">
          <span class="text-xs text-zinc-400 font-medium uppercase tracking-wider">Top Processes</span>
          <div class="mt-3 space-y-2">
            <div
              v-for="proc in system.processes.slice(0, 6)"
              :key="proc.pid"
              class="flex items-center justify-between text-xs"
            >
              <span class="text-zinc-300 truncate w-32">{{ proc.name }}</span>
              <span class="text-zinc-500">{{ proc.memory_mb }} MB</span>
              <span :class="proc.cpu_percent > 50 ? 'text-red-400' : 'text-zinc-400'">
                {{ proc.cpu_percent }}%
              </span>
            </div>
          </div>
        </div>

      </div>

      <!-- Footer -->
      <div class="px-4 py-2 border-t border-zinc-800 text-xs text-zinc-600 text-center">
        Auto-refresh every 3s
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useSystemStore } from '@/stores/system'
const system = useSystemStore()

function barColor(percent) {
  if (percent >= 85) return 'bg-red-500'
  if (percent >= 60) return 'bg-yellow-500'
  return 'bg-blue-500'
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  width: 0;
  opacity: 0;
}
</style>