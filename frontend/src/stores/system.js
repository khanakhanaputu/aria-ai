import { defineStore } from 'pinia'
import { ref } from 'vue'
import { systemAPI } from '@/services/api'

export const useSystemStore = defineStore('system', () => {
  const cpu = ref(null)
  const ram = ref(null)
  const gpu = ref([])
  const processes = ref([])
  const isVisible = ref(false)
  let intervalId = null

  async function fetchStatus() {
    try {
      const res = await systemAPI.getStatus()
      cpu.value = res.data.cpu
      ram.value = res.data.ram
      gpu.value = res.data.gpu
      processes.value = res.data.top_processes
    } catch (e) {
      console.error('Failed to fetch system status', e)
    }
  }

  function startPolling() {
    fetchStatus()
    intervalId = setInterval(fetchStatus, 3000)
  }

  function stopPolling() {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
  }

  function toggle() {
    isVisible.value = !isVisible.value
    if (isVisible.value) {
      startPolling()
    } else {
      stopPolling()
    }
  }

  return {
    cpu, ram, gpu, processes,
    isVisible, fetchStatus,
    startPolling, stopPolling, toggle,
  }
})