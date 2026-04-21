<template>
  <div class="p-4 border-t border-zinc-800">
    <div class="flex gap-3 items-end bg-zinc-800 rounded-2xl px-4 py-3 border border-zinc-700 focus-within:border-zinc-500 transition-colors">
      <textarea
        ref="inputRef"
        v-model="input"
        @keydown.enter.exact.prevent="send"
        @keydown.enter.shift.exact="input += '\n'"
        @input="resize"
        placeholder="Message Aria... (Enter to send, Shift+Enter for newline)"
        rows="1"
        class="flex-1 bg-transparent text-white text-sm placeholder-zinc-500 resize-none outline-none leading-relaxed max-h-40 overflow-y-auto"
      />
      <button
        @click="send"
        :disabled="!input.trim() || store.isStreaming"
        class="shrink-0 w-8 h-8 rounded-xl flex items-center justify-center transition-colors"
        :class="input.trim() && !store.isStreaming
          ? 'bg-blue-600 hover:bg-blue-500 text-white'
          : 'bg-zinc-700 text-zinc-500 cursor-not-allowed'"
      >
        <span v-if="store.isStreaming" class="text-xs">⏸</span>
        <span v-else>↑</span>
      </button>
    </div>
    <p class="text-xs text-zinc-600 text-center mt-2">
      Aria can make mistakes. Verify important information.
    </p>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'

const store = useChatStore()
const input = ref('')
const inputRef = ref(null)

async function send() {
  if (!input.value.trim() || store.isStreaming) return
  const text = input.value.trim()
  input.value = ''
  await nextTick()
  resize()
  await store.sendMessage(text)
}

function resize() {
  const el = inputRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = el.scrollHeight + 'px'
}
</script>