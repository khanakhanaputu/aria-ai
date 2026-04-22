<template>
  <div class="flex flex-col h-full bg-zinc-900 border-r border-zinc-800 w-64 shrink-0">
    <!-- Header -->
    <div class="p-4 border-b border-zinc-800">
      <h1 class="text-white font-semibold text-lg tracking-tight">Kane hitam</h1>
    </div>

    <!-- New Chat Button -->
    <div class="p-3">
      <button
        @click="store.newSession()"
        class="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-zinc-300 hover:bg-zinc-800 hover:text-white transition-colors border border-zinc-700 hover:border-zinc-600"
      >
        <span class="text-lg">+</span>
        New Chat
      </button>
    </div>

    <!-- Session List -->
    <div class="flex-1 overflow-y-auto px-3 pb-3 space-y-1">
      <div
        v-for="session in store.sessions"
        :key="session.id"
        @click="store.selectSession(session.id)"
        class="group flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-colors text-sm"
        :class="session.id === store.activeSessionId
          ? 'bg-zinc-700 text-white'
          : 'text-zinc-400 hover:bg-zinc-800 hover:text-white'"
      >
        <span class="truncate flex-1">{{ session.title }}</span>
        <button
          @click.stop="store.deleteSession(session.id)"
          class="opacity-0 group-hover:opacity-100 text-zinc-500 hover:text-red-400 transition-all ml-2 shrink-0"
        >
          ✕
        </button>
      </div>

      <div v-if="store.sessions.length === 0" class="text-zinc-600 text-xs text-center pt-4">
        No conversations yet
      </div>
    </div>

    <!-- Footer -->
    <!-- Footer -->
<div class="p-3 border-t border-zinc-800 space-y-2">
  <RouterLink
    to="/settings"
    class="flex items-center gap-2 px-3 py-2 rounded-lg text-zinc-500 hover:text-white hover:bg-zinc-800 transition-colors text-sm"
  >
    ⚙️ Settings
  </RouterLink>
  <div class="text-xs text-zinc-600 text-center">
    qwen2.5:3b · localhost
  </div>
</div>
  </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chat'
const store = useChatStore()
</script>