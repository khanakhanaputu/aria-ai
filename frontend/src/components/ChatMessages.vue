<template>
  <div ref="container" class="flex-1 overflow-y-auto px-6 py-4 space-y-6">
    <!-- Empty state -->
    <div v-if="store.messages.length === 0 && !store.isStreaming" class="flex flex-col items-center justify-center h-full text-center">
      <div class="text-4xl mb-4">🤖</div>
      <h2 class="text-white font-semibold text-xl mb-2">Aria AI</h2>
      <p class="text-zinc-500 text-sm">Start a conversation or type a command</p>
    </div>

    <!-- Messages -->
    <div v-for="(msg, i) in store.messages" :key="i">
      <!-- User bubble -->
      <div v-if="msg.role === 'user'" class="flex justify-end">
        <div class="max-w-[70%] px-4 py-3 rounded-2xl rounded-tr-sm bg-blue-600 text-white text-sm leading-relaxed">
          {{ msg.content }}
        </div>
      </div>

      <!-- AI bubble -->
      <div v-else class="flex gap-3">
        <div class="w-7 h-7 rounded-full bg-zinc-700 flex items-center justify-center shrink-0 mt-1 text-xs">
          🤖
        </div>
        <div class="max-w-[80%] text-sm text-zinc-200 leading-relaxed">
          <template v-for="(part, j) in parseContent(msg.content)" :key="j">
            <CodeBlock v-if="part.type === 'code'" :code="part.content" :language="part.language" />
            <div v-else class="prose prose-invert prose-sm max-w-none" v-html="renderMarkdown(part.content)" />
          </template>
        </div>
      </div>
    </div>

    <!-- Streaming bubble -->
    <div v-if="store.isStreaming" class="flex gap-3">
      <div class="w-7 h-7 rounded-full bg-zinc-700 flex items-center justify-center shrink-0 mt-1 text-xs">
        🤖
      </div>
      <div class="max-w-[80%] text-sm text-zinc-200 leading-relaxed">
        <span v-if="store.streamingMessage">{{ store.streamingMessage }}</span>
        <span v-else class="flex gap-1 mt-2">
          <span class="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
          <span class="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
          <span class="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { marked } from 'marked'
import { useChatStore } from '@/stores/chat'
import CodeBlock from './CodeBlock.vue'

const store = useChatStore()
const container = ref(null)

function renderMarkdown(text) {
  return marked.parse(text || '')
}
function parseContent(content) {
  const parts = []
  const codeBlockRegex = /```(\w*)\n?([\s\S]*?)```/g
  let lastIndex = 0
  let match

  while ((match = codeBlockRegex.exec(content)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: 'text', content: content.slice(lastIndex, match.index) })
    }
    parts.push({
      type: 'code',
      language: match[1] || 'plaintext',
      content: match[2].trim()
    })
    lastIndex = match.index + match[0].length
  }

  if (lastIndex < content.length) {
    parts.push({ type: 'text', content: content.slice(lastIndex) })
  }

  return parts.length ? parts : [{ type: 'text', content }]
}

// Auto scroll ke bawah
watch(
  () => [store.messages.length, store.streamingMessage],
  async () => {
    await nextTick()
    if (container.value) {
      container.value.scrollTop = container.value.scrollHeight
    }
  }
)
</script>