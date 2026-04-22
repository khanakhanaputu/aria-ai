<template>
  <div class="p-4 border-t border-zinc-800">

    <!-- File attachment preview -->
    <div v-if="store.attachedFile" class="flex items-center gap-2 mb-2 px-3 py-2 bg-zinc-800 rounded-xl border border-zinc-700">
      <span class="text-xs">📎</span>
      <span class="text-xs text-zinc-300 truncate flex-1">{{ store.attachedFile.name }}</span>
      <span v-if="store.attachedFile.trimmed" class="text-xs text-yellow-500">trimmed</span>
      <button @click="store.clearAttachment()" class="text-zinc-500 hover:text-red-400 transition-colors text-xs">✕</button>
    </div>

    <div class="flex gap-3 items-end bg-zinc-800 rounded-2xl px-4 py-3 border border-zinc-700 focus-within:border-zinc-500 transition-colors">

      <!-- Attach button -->
      <button
        @click="triggerFileInput"
        class="shrink-0 text-zinc-500 hover:text-white transition-colors mb-0.5"
        title="Attach file"
      >
        📎
      </button>
      <input
        ref="fileInputRef"
        type="file"
        class="hidden"
        accept=".py,.js,.ts,.vue,.jsx,.tsx,.html,.css,.json,.yaml,.yml,.md,.txt,.env,.ini,.cfg,.toml,.sh,.bat,.sql,.xml,.csv,.c,.cpp,.h,.java,.go,.rs,.php,.rb,.pdf"
        @change="handleFileChange"
      />

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
        <span v-if="store.isStreaming">⏸</span>
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
const fileInputRef = ref(null)
const uploadError = ref('')

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

function triggerFileInput() {
  fileInputRef.value?.click()
}

async function handleFileChange(e) {
  const file = e.target.files[0]
  if (!file) return
  const result = await store.attachFile(file)
  if (!result.success) {
    alert(`Failed to read file: ${result.error}`)
  }
  e.target.value = ''
}
</script>