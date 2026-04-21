<template>
  <Transition name="slide-up">
    <div
      v-if="runner.isVisible"
      class="absolute bottom-20 left-1/2 -translate-x-1/2 w-full max-w-2xl bg-zinc-900 border border-zinc-700 rounded-2xl shadow-2xl z-50 overflow-hidden"
    >
      <!-- Header -->
      <div class="flex items-center justify-between px-5 py-3 border-b border-zinc-800">
        <div class="flex items-center gap-2">
          <span class="text-sm">⚡</span>
          <h2 class="text-white font-semibold text-sm">Command Runner</h2>
        </div>
        <button @click="runner.toggle()" class="text-zinc-500 hover:text-white transition-colors">✕</button>
      </div>

      <div class="p-5 space-y-4">
        <!-- Input -->
        <div class="flex gap-2">
          <input
            v-model="runner.instruction"
            @keydown.enter="runner.parse()"
            placeholder="Describe what you want to do... (e.g. 'create a folder named MyProject on desktop')"
            class="flex-1 bg-zinc-800 text-white text-sm px-4 py-2.5 rounded-xl border border-zinc-700 focus:border-zinc-500 outline-none placeholder-zinc-600"
          />
          <button
            @click="runner.parse()"
            :disabled="runner.isParsing || !runner.instruction.trim()"
            class="px-4 py-2.5 rounded-xl text-sm font-medium transition-colors"
            :class="runner.isParsing || !runner.instruction.trim()
              ? 'bg-zinc-700 text-zinc-500 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-500 text-white'"
          >
            {{ runner.isParsing ? 'Parsing...' : 'Parse' }}
          </button>
        </div>

        <!-- Parsed Command Preview -->
        <div v-if="runner.parsedCommand" class="rounded-xl border overflow-hidden"
          :class="{
            'border-green-700 bg-green-950': runner.parsedCommand.status === 'ready',
            'border-red-700 bg-red-950': runner.parsedCommand.status === 'blocked' || runner.parsedCommand.status === 'unsafe',
            'border-zinc-700 bg-zinc-800': runner.parsedCommand.status === 'error',
          }"
        >
          <div class="px-4 py-2 border-b flex items-center gap-2"
            :class="{
              'border-green-700': runner.parsedCommand.status === 'ready',
              'border-red-700': runner.parsedCommand.status === 'blocked' || runner.parsedCommand.status === 'unsafe',
              'border-zinc-700': runner.parsedCommand.status === 'error',
            }"
          >
            <span v-if="runner.parsedCommand.status === 'ready'" class="text-green-400 text-xs font-medium">✓ Safe to execute</span>
            <span v-else class="text-red-400 text-xs font-medium">✕ {{ runner.parsedCommand.reason }}</span>
          </div>
          <div class="px-4 py-3 font-mono text-sm"
            :class="runner.parsedCommand.status === 'ready' ? 'text-green-300' : 'text-red-300'"
          >
            {{ runner.parsedCommand.command || runner.parsedCommand.reason }}
          </div>
        </div>

        <!-- Execute Button -->
        <div v-if="runner.parsedCommand?.status === 'ready'" class="flex gap-2">
          <button
            @click="runner.execute()"
            :disabled="runner.isExecuting"
            class="flex-1 py-2.5 rounded-xl text-sm font-medium transition-colors"
            :class="runner.isExecuting
              ? 'bg-zinc-700 text-zinc-500 cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-500 text-white'"
          >
            {{ runner.isExecuting ? 'Executing...' : '▶ Execute Command' }}
          </button>
          <button
            @click="runner.reset()"
            class="px-4 py-2.5 rounded-xl text-sm text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
          >
            Cancel
          </button>
        </div>

        <!-- Result -->
        <div v-if="runner.result" class="rounded-xl border border-zinc-700 overflow-hidden">
          <div class="px-4 py-2 border-b border-zinc-700 flex items-center gap-2">
            <span
              class="text-xs font-medium"
              :class="{
                'text-green-400': runner.result.status === 'success',
                'text-red-400': runner.result.status === 'error' || runner.result.status === 'blocked',
                'text-yellow-400': runner.result.status === 'timeout',
              }"
            >
              {{ runner.result.status.toUpperCase() }}
            </span>
          </div>
          <pre class="px-4 py-3 text-xs text-zinc-300 font-mono whitespace-pre-wrap max-h-32 overflow-y-auto bg-zinc-950">{{ runner.result.output }}</pre>
        </div>

        <!-- Recent Logs -->
        <div v-if="runner.logs.length > 0">
          <p class="text-xs text-zinc-600 uppercase tracking-wider mb-2">Recent Commands</p>
          <div class="space-y-1 max-h-32 overflow-y-auto">
            <div
              v-for="log in runner.logs.slice(0, 5)"
              :key="log.id"
              class="flex items-center gap-3 px-3 py-2 rounded-lg bg-zinc-800 text-xs"
            >
              <span
                class="w-1.5 h-1.5 rounded-full shrink-0"
                :class="{
                  'bg-green-500': log.status === 'success',
                  'bg-red-500': log.status === 'error' || log.status === 'blocked',
                  'bg-yellow-500': log.status === 'timeout',
                }"
              />
              <span class="font-mono text-zinc-300 truncate flex-1">{{ log.command }}</span>
              <span class="text-zinc-600 shrink-0">{{ log.status }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useRunnerStore } from '@/stores/runner'
const runner = useRunnerStore()
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateX(-50%) translateY(20px);
  opacity: 0;
}
</style>