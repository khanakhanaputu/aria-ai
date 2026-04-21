import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { chatAPI } from '@/services/api'

export const useChatStore = defineStore('chat', () => {
  const sessions = ref([])
  const activeSessionId = ref(null)
  const messages = ref([])
  const isStreaming = ref(false)
  const streamingMessage = ref('')

  const activeSession = computed(() =>
    sessions.value.find(s => s.id === activeSessionId.value)
  )

  async function loadSessions() {
    const res = await chatAPI.getSessions()
    sessions.value = res.data
  }

  async function selectSession(id) {
    activeSessionId.value = id
    const res = await chatAPI.getMessages(id)
    messages.value = res.data
  }

  async function newSession() {
    const res = await chatAPI.createSession()
    await loadSessions()
    await selectSession(res.data.session_id)
  }

  async function deleteSession(id) {
    await chatAPI.deleteSession(id)
    if (activeSessionId.value === id) {
      activeSessionId.value = null
      messages.value = []
    }
    await loadSessions()
  }

  async function sendMessage(text) {
    if (!text.trim() || isStreaming.value) return

    // Tambah pesan user ke UI langsung
    messages.value.push({ role: 'user', content: text })

    // Siapkan placeholder AI
    isStreaming.value = true
    streamingMessage.value = ''

    await chatAPI.streamMessage(
      text,
      activeSessionId.value,
      (token) => {
        streamingMessage.value += token
      },
      async (fullText, sessionId) => {
        // Simpan ke messages
        messages.value.push({ role: 'assistant', content: fullText })
        streamingMessage.value = ''
        isStreaming.value = false

        // Update session ID kalau baru
        if (!activeSessionId.value) {
          activeSessionId.value = sessionId
          await loadSessions()
        }
      }
    )
  }

  return {
    sessions,
    activeSessionId,
    messages,
    isStreaming,
    streamingMessage,
    activeSession,
    loadSessions,
    selectSession,
    newSession,
    deleteSession,
    sendMessage,
  }
})