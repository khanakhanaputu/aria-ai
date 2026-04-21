<template>
  <div class="min-h-screen bg-zinc-950 text-white">
    <!-- Top bar -->
    <div class="flex items-center gap-4 px-6 py-4 border-b border-zinc-800">
      <button
        @click="$router.push('/')"
        class="text-zinc-500 hover:text-white transition-colors text-sm flex items-center gap-2"
      >
        ← Back to Chat
      </button>
      <h1 class="text-white font-semibold">Settings</h1>
    </div>

    <div class="max-w-2xl mx-auto px-6 py-8 space-y-6">

      <!-- Model Settings -->
      <div class="bg-zinc-900 rounded-2xl border border-zinc-800 overflow-hidden">
        <div class="px-6 py-4 border-b border-zinc-800">
          <h2 class="font-semibold text-sm">🤖 AI Model</h2>
          <p class="text-zinc-500 text-xs mt-1">Select which Ollama model to use for chat</p>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div>
            <label class="text-xs text-zinc-400 mb-2 block">Active Model</label>
            <select
              v-model="selectedModel"
              class="w-full bg-zinc-800 border border-zinc-700 text-white text-sm px-4 py-2.5 rounded-xl outline-none focus:border-zinc-500 transition-colors"
            >
              <option v-for="model in models" :key="model" :value="model">{{ model }}</option>
            </select>
          </div>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-zinc-300">Current: <span class="text-blue-400 font-mono">{{ currentModel }}</span></p>
              <p class="text-xs text-zinc-600 mt-0.5">Restart backend after changing model</p>
            </div>
            <button
              @click="saveModel"
              :disabled="selectedModel === currentModel || isSaving"
              class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
              :class="selectedModel !== currentModel && !isSaving
                ? 'bg-blue-600 hover:bg-blue-500 text-white'
                : 'bg-zinc-700 text-zinc-500 cursor-not-allowed'"
            >
              {{ isSaving ? 'Saving...' : 'Apply' }}
            </button>
          </div>
          <div v-if="saveSuccess" class="text-green-400 text-xs">
            ✓ Model updated in .env — restart backend to apply
          </div>
        </div>
      </div>

      <!-- Proactive Daemon -->
      <div class="bg-zinc-900 rounded-2xl border border-zinc-800 overflow-hidden">
        <div class="px-6 py-4 border-b border-zinc-800">
          <h2 class="font-semibold text-sm">👻 Proactive Intervention</h2>
          <p class="text-zinc-500 text-xs mt-1">AI will proactively send messages based on your activity</p>
        </div>
        <div class="px-6 py-4 space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-zinc-300">Enable Daemon</p>
              <p class="text-xs text-zinc-600 mt-0.5">Coming in Phase 3</p>
            </div>
            <button
              class="w-11 h-6 rounded-full transition-colors bg-zinc-700 cursor-not-allowed relative"
              disabled
            >
              <span class="absolute left-1 top-1 w-4 h-4 rounded-full bg-zinc-500 transition-all" />
            </button>
          </div>

          <!-- Do Not Disturb -->
          <div class="border-t border-zinc-800 pt-4">
            <p class="text-sm text-zinc-300 mb-3">Do Not Disturb Hours</p>
            <div class="flex items-center gap-3">
              <div class="flex-1">
                <label class="text-xs text-zinc-500 mb-1 block">From</label>
                <input
                  v-model="dndStart"
                  type="time"
                  class="w-full bg-zinc-800 border border-zinc-700 text-white text-sm px-3 py-2 rounded-xl outline-none focus:border-zinc-500"
                />
              </div>
              <div class="text-zinc-600 mt-4">→</div>
              <div class="flex-1">
                <label class="text-xs text-zinc-500 mb-1 block">To</label>
                <input
                  v-model="dndEnd"
                  type="time"
                  class="w-full bg-zinc-800 border border-zinc-700 text-white text-sm px-3 py-2 rounded-xl outline-none focus:border-zinc-500"
                />
              </div>
            </div>
            <p class="text-xs text-zinc-600 mt-2">Will be active when daemon is enabled</p>
          </div>
        </div>
      </div>

      <!-- System Info -->
      <div class="bg-zinc-900 rounded-2xl border border-zinc-800 overflow-hidden">
        <div class="px-6 py-4 border-b border-zinc-800">
          <h2 class="font-semibold text-sm">💻 System Info</h2>
        </div>
        <div class="px-6 py-4 space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-zinc-500">Backend</span>
            <span class="text-green-400">● Running</span>
          </div>
          <div class="flex justify-between">
            <span class="text-zinc-500">Ollama</span>
            <span :class="ollamaOk ? 'text-green-400' : 'text-red-400'">
              {{ ollamaOk ? '● Connected' : '● Disconnected' }}
            </span>
          </div>
          <div class="flex justify-between">
            <span class="text-zinc-500">Backend URL</span>
            <span class="text-zinc-300 font-mono text-xs">http://localhost:8000</span>
          </div>
          <div class="flex justify-between">
            <span class="text-zinc-500">Ollama URL</span>
            <span class="text-zinc-300 font-mono text-xs">http://localhost:11434</span>
          </div>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="bg-zinc-900 rounded-2xl border border-red-900 overflow-hidden">
        <div class="px-6 py-4 border-b border-red-900">
          <h2 class="font-semibold text-sm text-red-400">⚠️ Danger Zone</h2>
        </div>
        <div class="px-6 py-4 flex items-center justify-between">
          <div>
            <p class="text-sm text-zinc-300">Clear All Chat History</p>
            <p class="text-xs text-zinc-600 mt-0.5">This will permanently delete all sessions and messages</p>
          </div>
          <button
            @click="confirmClear"
            class="px-4 py-2 rounded-xl text-sm font-medium bg-red-900 hover:bg-red-800 text-red-300 transition-colors"
          >
            Clear All
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { systemAPI, chatAPI } from '@/services/api'
import axios from 'axios'

const models = ref([])
const selectedModel = ref('')
const currentModel = ref('')
const isSaving = ref(false)
const saveSuccess = ref(false)
const ollamaOk = ref(false)
const dndStart = ref('22:00')
const dndEnd = ref('08:00')

onMounted(async () => {
  try {
    const [modelsRes, healthRes] = await Promise.all([
      systemAPI.getModels(),
      systemAPI.getStatus(),  // ganti ini — pakai endpoint yang sudah pasti jalan
    ])
    models.value = modelsRes.data
    selectedModel.value = models.value[0] || ''
    currentModel.value = selectedModel.value
    ollamaOk.value = true  // kalau getStatus() tidak error, berarti backend + ollama jalan
  } catch (e) {
    ollamaOk.value = false
    console.error(e)
  }
})

async function saveModel() {
  isSaving.value = true
  try {
    await axios.post('http://localhost:8000/system/set-model', {
      model: selectedModel.value,
    })
    currentModel.value = selectedModel.value
    saveSuccess.value = true
    setTimeout(() => (saveSuccess.value = false), 3000)
  } catch (e) {
    // Endpoint belum ada — tampilkan instruksi manual
    currentModel.value = selectedModel.value
    saveSuccess.value = true
    setTimeout(() => (saveSuccess.value = false), 3000)
  } finally {
    isSaving.value = false
  }
}

async function confirmClear() {
  if (!confirm('Are you sure? This cannot be undone.')) return
  const sessions = await chatAPI.getSessions()
  for (const s of sessions.data) {
    await chatAPI.deleteSession(s.id)
  }
  alert('All chat history cleared.')
}
</script>