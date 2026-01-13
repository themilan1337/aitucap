import { defineStore } from 'pinia'

export const useOnboardingStore = defineStore('onboarding', () => {
  const goal = ref<string | null>(null)
  const level = ref<string | null>(null)
  const gender = ref<string | null>(null)
  const height = ref<number | null>(null)
  const weight = ref<number | null>(null)
  const age = ref<number | null>(null)
  const status = ref<'idle' | 'loading' | 'ready' | 'error'>('idle')
  const completed = ref(false)

  function setGoal(newGoal: string) {
    goal.value = newGoal
  }

  function setLevel(newLevel: string) {
    level.value = newLevel
  }

  function setGender(newGender: string) {
    gender.value = newGender
  }

  function setPhysicalParams(params: { height?: number; weight?: number; age?: number }) {
    if (params.height !== undefined) height.value = params.height
    if (params.weight !== undefined) weight.value = params.weight
    if (params.age !== undefined) age.value = params.age
  }

  function completeOnboarding() {
    completed.value = true
  }

  function resetOnboarding() {
    goal.value = null
    level.value = null
    gender.value = null
    height.value = null
    weight.value = null
    age.value = null
    completed.value = false
  }

  return {
    goal,
    level,
    gender,
    height,
    weight,
    age,
    status,
    completed,
    setGoal,
    setLevel,
    setGender,
    setPhysicalParams,
    completeOnboarding,
    resetOnboarding
  }
}, {
  persist: true
})
