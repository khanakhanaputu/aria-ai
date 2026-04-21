import { defineStore } from 'pinia'
import { ref } from 'vue'
import { runnerAPI } from '@/services/api'

export const useRunnerStore = defineStore('runner', () => {
  const isVisible = ref(false)
  const instruction = ref('')
  const parsedCommand = ref(null)
  const result = ref(null)
  const logs = ref([])
  const isParsing = ref(false)
  const isExecuting = ref(false)

  function toggle() {
    isVisible.value = !isVisible.value
    if (isVisible.value) fetchLogs()
  }

  async function parse() {
    if (!instruction.value.trim()) return
    isParsing.value = true
    parsedCommand.value = null
    result.value = null
    try {
      const res = await runnerAPI.parse(instruction.value)
      parsedCommand.value = res.data
    } catch (e) {
      parsedCommand.value = { status: 'error', reason: e.message }
    } finally {
      isParsing.value = false
    }
  }

  async function execute() {
    if (!parsedCommand.value?.command) return
    isExecuting.value = true
    try {
      const res = await runnerAPI.execute(parsedCommand.value.command)
      result.value = res.data
      await fetchLogs()
    } catch (e) {
      result.value = { status: 'error', output: e.message }
    } finally {
      isExecuting.value = false
    }
  }

  async function fetchLogs() {
    try {
      const res = await runnerAPI.getLogs()
      logs.value = res.data
    } catch (e) {
      console.error(e)
    }
  }

  function reset() {
    instruction.value = ''
    parsedCommand.value = null
    result.value = null
  }

  return {
    isVisible, instruction, parsedCommand,
    result, logs, isParsing, isExecuting,
    toggle, parse, execute, fetchLogs, reset,
  }
})