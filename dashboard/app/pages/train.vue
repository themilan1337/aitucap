<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import SectionTitle from '~/components/SectionTitle.vue'
import ExerciseCard from '~/components/ExerciseCard.vue'
import WorkoutCamera from '~/components/workout/WorkoutCamera.vue'
import type { WorkoutPlan } from '~/composables/usePlan'

// Get query params
const route = useRoute()
const planDayId = computed(() => route.query.plan_day_id as string | undefined)

// State
const plan = ref<WorkoutPlan | null>(null)
const isTrainingStarted = ref(false)
const loading = ref(true)
const error = ref<string | null>(null)

// Get composables
const { fetchActivePlan } = usePlan()

// Exercise name mapping
const exerciseNames: Record<string, string> = {
  squat: 'Приседания',
  lunge: 'Выпады',
  pushup: 'Отжимания',
  plank: 'Планка',
  situp: 'Подъемы корпуса',
  crunch: 'Скручивания',
  bicep_curl: 'Сгибания на бицепс',
  lateral_raise: 'Боковые подъемы',
  overhead_press: 'Жим над головой',
  leg_raise: 'Подъемы ног',
  knee_raise: 'Подъемы коленей',
  knee_press: 'Жим коленями'
}

/**
 * Get today's plan day based on plan_day_id or current date
 */
const todayPlanDay = computed(() => {
  if (!plan.value || !plan.value.days) return null

  // If plan_day_id is provided, use it
  if (planDayId.value) {
    return plan.value.days.find(d => d.id === planDayId.value)
  }

  // Otherwise, calculate today's day based on start date
  const startDate = new Date(plan.value.week_start_date)
  const today = new Date()
  const diffTime = today.getTime() - startDate.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  const dayNumber = Math.max(0, Math.min(29, diffDays))

  return plan.value.days.find(d => d.day_number === dayNumber)
})

/**
 * Get today's exercises formatted for UI
 */
const todayExercises = computed(() => {
  if (!todayPlanDay.value || todayPlanDay.value.is_rest_day) return []

  return todayPlanDay.value.exercises.map(ex => ({
    id: ex.id,
    name: exerciseNames[ex.exercise_type] || ex.exercise_type,
    sets: ex.target_sets,
    reps: ex.target_reps,
    type: ex.exercise_type // Keep original type for camera
  }))
})

/**
 * Estimated duration
 */
const estimatedDuration = computed(() => {
  return todayExercises.value.length * 5 // ~5 min per exercise
})

/**
 * Load plan data
 */
const loadPlan = async () => {
  try {
    loading.value = true
    error.value = null
    plan.value = await fetchActivePlan()

    // Check if plan day exists
    if (!todayPlanDay.value) {
      error.value = 'Не найдена тренировка на сегодня'
    }
  } catch (err: any) {
    console.error('Failed to load plan:', err)
    error.value = err.message || 'Не удалось загрузить план'
  } finally {
    loading.value = false
  }
}

/**
 * Start training
 */
const startTraining = () => {
  isTrainingStarted.value = true
}

/**
 * End training
 */
const endTraining = () => {
  isTrainingStarted.value = false
  // Navigate back to home
  navigateTo('/home')
}

onMounted(() => {
  loadPlan()
})
</script>

<template>
  <div class="min-h-screen bg-black pb-20">
    <!-- Loading State -->
    <div v-if="loading && !isTrainingStarted" class="flex items-center justify-center min-h-screen">
      <Icon icon="heroicons:arrow-path" class="w-8 h-8 animate-spin text-neon" />
    </div>

    <!-- Error State -->
    <div v-else-if="error && !isTrainingStarted" class="px-4 pt-12">
      <div class="bg-red-500/10 border border-red-500 rounded-xl p-4 mb-6">
        <p class="text-red-500">{{ error }}</p>
        <div class="flex gap-3 mt-4">
          <button
            @click="loadPlan"
            class="px-4 py-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 text-sm"
          >
            Повторить
          </button>
          <router-link
            to="/plan"
            class="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-sm"
          >
            К плану
          </router-link>
        </div>
      </div>
    </div>

    <!-- Rest Day -->
    <div v-else-if="todayPlanDay?.is_rest_day && !isTrainingStarted" class="px-4 pt-12">
      <div class="text-center py-16">
        <Icon icon="heroicons:moon" class="w-20 h-20 mx-auto mb-6 text-neon" />
        <h1 class="text-3xl font-bold mb-3">День отдыха</h1>
        <p class="text-gray-400 mb-8">Восстановление - важная часть прогресса</p>
        <router-link
          to="/home"
          class="inline-block px-6 py-3 rounded-xl bg-neon text-black font-bold hover:brightness-110 transition"
        >
          На главную
        </router-link>
      </div>
    </div>

    <!-- Training Preview (Before Starting) -->
    <div v-else-if="!isTrainingStarted && todayExercises.length > 0" class="px-4 pt-12 pb-8">
      <header class="flex justify-between items-start mb-6">
        <div>
          <p class="text-gray-400 text-sm mb-1">Готовы к тренировке?</p>
          <h1 class="text-3xl font-bold">Начнем!</h1>
        </div>
        <router-link
          to="/home"
          class="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition"
        >
          <Icon icon="heroicons:x-mark" class="w-5 h-5" />
        </router-link>
      </header>

      <!-- Today's Training Plan -->
      <div class="mb-8">
        <div class="bg-[#111] rounded-3xl p-5">
          <!-- Exercises List -->
          <div class="mb-4 border border-white/5 rounded-xl">
            <ExerciseCard
              v-for="exercise in todayExercises"
              :key="exercise.id"
              :name="exercise.name"
              :sets="exercise.sets"
              :reps="exercise.reps"
              icon="heroicons:bolt"
            />
          </div>

          <!-- Metadata -->
          <div class="flex justify-between items-center text-sm text-gray-400 px-1 mb-6">
            <div class="flex items-center gap-2">
              <Icon icon="heroicons:clock" class="text-neon" />
              <span>~{{ estimatedDuration }} мин</span>
            </div>
            <div class="flex items-center gap-2">
              <Icon icon="heroicons:fire" class="text-neon" />
              <span>{{ todayExercises.length }} упр.</span>
            </div>
          </div>

          <!-- Start Training Button -->
          <button
            @click="startTraining"
            class="w-full py-4 rounded-xl bg-neon text-black font-bold text-lg flex items-center justify-center gap-2 hover:brightness-110 active:scale-[0.98] transition-all"
          >
            <Icon icon="heroicons:play" />
            Начать тренировку
          </button>
        </div>
      </div>

      <!-- Training Tips -->
      <div class="bg-[#111] rounded-2xl p-5">
        <h3 class="text-white font-bold mb-3 flex items-center gap-2">
          <Icon icon="heroicons:light-bulb" class="text-neon text-xl" />
          Советы перед началом
        </h3>
        <ul class="space-y-2 text-sm text-gray-400">
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:check-circle" class="text-neon mt-0.5 flex-shrink-0" />
            <span>Убедитесь, что камера видит вас полностью</span>
          </li>
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:check-circle" class="text-neon mt-0.5 flex-shrink-0" />
            <span>Выберите хорошо освещенное место</span>
          </li>
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:check-circle" class="text-neon mt-0.5 flex-shrink-0" />
            <span>Держите телефон в вертикальном положении</span>
          </li>
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:check-circle" class="text-neon mt-0.5 flex-shrink-0" />
            <span>Следите за подсказками по технике выполнения</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- No Exercises -->
    <div v-else-if="!isTrainingStarted" class="px-4 pt-12">
      <div class="text-center py-16">
        <Icon icon="heroicons:calendar" class="w-20 h-20 mx-auto mb-6 text-gray-600" />
        <h1 class="text-3xl font-bold mb-3">Нет упражнений</h1>
        <p class="text-gray-400 mb-8">Создайте план тренировок</p>
        <router-link
          to="/plan"
          class="inline-block px-6 py-3 rounded-xl bg-neon text-black font-bold hover:brightness-110 transition"
        >
          К плану
        </router-link>
      </div>
    </div>

    <!-- Training Started - Show Camera -->
    <WorkoutCamera
      v-if="isTrainingStarted"
      :exercises="todayExercises"
      :plan-day-id="planDayId"
      @end-training="endTraining"
    />
  </div>
</template>

<style scoped>
.text-neon {
  color: var(--color-neon);
}
.bg-neon {
  background-color: var(--color-neon);
}
.bg-neon\/10 {
  background-color: rgba(204, 255, 0, 0.1);
}
</style>
