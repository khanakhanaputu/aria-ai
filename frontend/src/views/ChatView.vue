<template>
  <div class="flex h-screen bg-zinc-950">
    <ChatSidebar />
    <div class="flex flex-col flex-1 min-w-0">
      <!-- Top bar -->
      <div class="flex items-center justify-between px-6 py-3 border-b border-zinc-800 shrink-0">
        <div class="text-sm text-zinc-400">
          {{ store.activeSession?.title || 'Select or start a conversation' }}
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="runner.toggle()"
            class="text-xs px-3 py-1.5 rounded-lg transition-colors"
            :class="runner.isVisible
              ? 'bg-zinc-700 text-white'
              : 'text-zinc-500 hover:text-white hover:bg-zinc-800'"
          >
            ⚡ Runner
          </button>
          <button
            @click="system.toggle()"
            class="text-xs px-3 py-1.5 rounded-lg transition-colors"
            :class="system.isVisible
              ? 'bg-zinc-700 text-white'
              : 'text-zinc-500 hover:text-white hover:bg-zinc-800'"
          >
            📊 System
          </button>
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-green-500"></div>
            <span class="text-xs text-zinc-500">Connected</span>
          </div>
        </div>
      </div>

      <div class="flex flex-1 min-h-0 relative">
        <div class="flex flex-col flex-1 min-w-0">
          <ChatMessages />
          <ChatInput />
        </div>
        <SystemPanel />
        <RunnerPanel />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useSystemStore } from '@/stores/system'
import { useRunnerStore } from '@/stores/runner'
import ChatSidebar from '@/components/ChatSidebar.vue'
import ChatMessages from '@/components/ChatMessages.vue'
import ChatInput from '@/components/ChatInput.vue'
import SystemPanel from '@/components/SystemPanel.vue'
import RunnerPanel from '@/components/RunnerPanel.vue'

const store = useChatStore()
const system = useSystemStore()
const runner = useRunnerStore()

onMounted(async () => {
  await store.loadSessions()
})
</script>