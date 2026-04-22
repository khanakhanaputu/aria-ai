import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 60000,
})

export const chatAPI = {
  // Sessions
  getSessions: () => api.get('/chat/sessions'),
  createSession: (title = 'New Chat') => api.post('/chat/sessions', { title }),
  deleteSession: (id) => api.delete(`/chat/sessions/${id}`),
  renameSession: (id, title) => api.patch(`/chat/sessions/${id}`, { title }),
  getMessages: (id) => api.get(`/chat/sessions/${id}/messages`),

  // Streaming chat
  streamMessage: async (message, sessionId, onToken, onDone) => {
    const response = await fetch('http://localhost:8000/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, session_id: sessionId }),
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let fullText = ''
    let extractedSessionId = sessionId

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })

      // Cek apakah chunk mengandung SESSION_ID marker
      const sessionMatch = chunk.match(/\[SESSION_ID:(\d+)\]/)
      if (sessionMatch) {
        extractedSessionId = parseInt(sessionMatch[1])
        const cleanChunk = chunk.replace(/\n\n\[SESSION_ID:\d+\]/, '')
        if (cleanChunk) {
          fullText += cleanChunk
          onToken(cleanChunk)
        }
      } else {
        fullText += chunk
        onToken(chunk)
      }
    }

    onDone(fullText, extractedSessionId)
  },
}

export const systemAPI = {
  getStatus: () => api.get('/system/'),
  getCpu: () => api.get('/system/cpu'),
  getRam: () => api.get('/system/ram'),
  getGpu: () => api.get('/system/gpu'),
  getProcesses: (limit = 10) => api.get(`/system/processes?limit=${limit}`),
}

export const runnerAPI = {
  parse: (instruction) => api.post('/runner/parse', { instruction }),
  execute: (command) => api.post('/runner/execute', { command }),
  getLogs: () => api.get('/runner/logs'),
}

export const filesAPI = {
  readFile: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/files/read', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
export default api