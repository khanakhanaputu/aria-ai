import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { chatAPI, filesAPI } from '@/services/api'

export const useChatStore = defineStore('chat', () => {
  const sessions = ref([])
  const activeSessionId = ref(null)
  const messages = ref([])
  const isStreaming = ref(false)
  const streamingMessage = ref('')
  const attachedFile = ref(null)  // { name, content, type }

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

  async function attachFile(file) {
    try {
      const res = await filesAPI.readFile(file)
      attachedFile.value = {
        name: res.data.filename,
        content: res.data.content,
        type: res.data.file_type,
        trimmed: res.data.trimmed,
      }
      return { success: true }
    } catch (e) {
      return { success: false, error: e.response?.data?.detail || e.message }
    }
  }

  function clearAttachment() {
    attachedFile.value = null
  }

  async function sendMessage(text) {
    if (!text.trim() || isStreaming.value) return

    let fullMessage = text

    // Inject file content ke message kalau ada attachment
    if (attachedFile.value) {
      fullMessage = `User attached a file: **${attachedFile.value.name}**\n\n\`\`\`\n${attachedFile.value.content}\n\`\`\`\n\nUser's message: ${text}`
      messages.value.push({
        role: 'user',
        content: text,
        attachment: attachedFile.value.name,
      })
      attachedFile.value = null
    } else {
      messages.value.push({ role: 'user', content: text })
    }

    isStreaming.value = true
    streamingMessage.value = ''

    await chatAPI.streamMessage(
      fullMessage,
      activeSessionId.value,
      (token) => {
        streamingMessage.value += token
      },
      async (fullText, sessionId) => {
        messages.value.push({ role: 'assistant', content: fullText })
        streamingMessage.value = ''
        isStreaming.value = false

        if (!activeSessionId.value) {
          activeSessionId.value = sessionId
        }
        await loadSessions()
      }
    )
  }

  return {
    sessions, activeSessionId, messages,
    isStreaming, streamingMessage, attachedFile,
    activeSession, loadSessions, selectSession,
    newSession, deleteSession, sendMessage,
    attachFile, clearAttachment,
  }
})