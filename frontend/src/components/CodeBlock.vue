<template>
  <div class="relative my-2 rounded-lg overflow-hidden border border-zinc-700">
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-2 bg-zinc-800 border-b border-zinc-700">
      <span class="text-xs text-zinc-400 font-mono">{{ language }}</span>
      <button
        @click="copy"
        class="text-xs text-zinc-400 hover:text-white transition-colors"
      >
        {{ copied ? '✓ Copied' : 'Copy' }}
      </button>
    </div>
    <!-- Code -->
    <pre class="p-4 overflow-x-auto bg-zinc-900 text-sm"><code v-html="highlighted"></code></pre>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const props = defineProps({
  code: { type: String, required: true },
  language: { type: String, default: 'plaintext' },
})

const copied = ref(false)

const highlighted = computed(() => {
  try {
    if (props.language && props.language !== 'plaintext') {
      return hljs.highlight(props.code, { language: props.language }).value
    }
    return hljs.highlightAuto(props.code).value
  } catch {
    return props.code
  }
})

async function copy() {
  await navigator.clipboard.writeText(props.code)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>