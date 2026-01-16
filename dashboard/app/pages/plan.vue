<script setup lang="ts">
import SectionTitle from '~/components/SectionTitle.vue'
import ExerciseCard from '~/components/ExerciseCard.vue'
import { Icon } from '@iconify/vue'
import { ref, computed, onMounted } from 'vue'
import type { WorkoutPlan, PlanDay } from '~/composables/usePlan'

// State
const plan = ref<WorkoutPlan | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const currentWeek = ref(0) // 0-3 for 4 weeks
const showRegenerateDialog = ref(false)
const regenerating = ref(false)

// Get composables
const { fetchActivePlan, generatePlan } = usePlan()

// Day names
const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

/**
 * Calculate which day number is today (0-29) based on plan start date
 */
const todayDayNumber = computed(() => {
  if (!plan.value) return 0

  const startDate = new Date(plan.value.week_start_date)
  const today = new Date()
  const diffTime = today.getTime() - startDate.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  // Clamp to 0-29 range
  return Math.max(0, Math.min(29, diffDays))
})

/**
 * Get 7 days for the current week (0-6, 7-13, 14-20, 21-29)
 */
const weekDays = computed(() => {
  if (!plan.value || !plan.value.days) return []

  const startIdx = currentWeek.value * 7
  const endIdx = Math.min(startIdx + 7, plan.value.days.length)

  return plan.value.days.slice(startIdx, endIdx).map(day => {
    const dayNumber = day.day_number
    const today = todayDayNumber.value

    let status = 'future'
    if (dayNumber === today) {
      status = 'today'
    } else if (dayNumber < today) {
      status = day.is_completed ? 'done' : 'missed'
    } else if (day.is_rest_day) {
      status = 'rest'
    }

    return {
      ...day,
      status,
      dayName: dayNames[dayNumber % 7]
    }
  })
})

/**
 * Get today's plan day
 */
const todayPlanDay = computed(() => {
  if (!plan.value || !plan.value.days) return null
  return plan.value.days.find(d => d.day_number === todayDayNumber.value)
})

/**
 * Get today's exercises
 */
const todayExercises = computed(() => {
  if (!todayPlanDay.value || todayPlanDay.value.is_rest_day) return []

  // Map exercise types to display names
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

  const exerciseIcons: Record<string, string> = {
    squat: 'heroicons:bolt',
    lunge: 'heroicons:fire',
    pushup: 'heroicons:arrow-trending-up',
    plank: 'heroicons:clock'
  }

  return todayPlanDay.value.exercises.map(ex => ({
    name: exerciseNames[ex.exercise_type] || ex.exercise_type,
    sets: ex.target_sets,
    reps: ex.target_reps,
    icon: exerciseIcons[ex.exercise_type] || 'heroicons:bolt'
  }))
})

/**
 * Progress bar: current day / 30
 */
const progressPercentage = computed(() => {
  return Math.round((todayDayNumber.value / 29) * 100)
})

/**
 * Week navigation
 */
const canGoToPreviousWeek = computed(() => currentWeek.value > 0)
const canGoToNextWeek = computed(() => currentWeek.value < 3 && plan.value?.days && plan.value.days.length > (currentWeek.value + 1) * 7)

const previousWeek = () => {
  if (canGoToPreviousWeek.value) {
    currentWeek.value--
  }
}

const nextWeek = () => {
  if (canGoToNextWeek.value) {
    currentWeek.value++
  }
}

/**
 * Fetch plan on mount
 */
const loadPlan = async () => {
  try {
    loading.value = true
    error.value = null
    plan.value = await fetchActivePlan()

    // Set current week based on today's day number
    currentWeek.value = Math.floor(todayDayNumber.value / 7)
  } catch (err: any) {
    console.error('Failed to load plan:', err)
    error.value = err.message || 'Не удалось загрузить план'
  } finally {
    loading.value = false
  }
}

/**
 * Regenerate plan
 */
const handleRegeneratePlan = async () => {
  try {
    regenerating.value = true
    await generatePlan()
    showRegenerateDialog.value = false
    // Reload plan
    await loadPlan()
  } catch (err: any) {
    console.error('Failed to regenerate plan:', err)
    error.value = err.message || 'Не удалось создать новый план'
  } finally {
    regenerating.value = false
  }
}

/**
 * Start training
 */
const startTraining = () => {
  if (!todayPlanDay.value || todayPlanDay.value.is_rest_day) return

  navigateTo({
    path: '/train',
    query: {
      plan_day_id: todayPlanDay.value.id
    }
  })
}

onMounted(() => {
  loadPlan()
})
</script>

<template>
  <div class="px-4 pt-12 pb-8">
     <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold">План тренировок</h1>
        <button
          @click="showRegenerateDialog = true"
          class="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition"
        >
          <Icon icon="heroicons:arrow-path" class="w-5 h-5" />
        </button>
     </div>

     <!-- Loading State -->
     <div v-if="loading" class="flex items-center justify-center py-20">
        <Icon icon="heroicons:arrow-path" class="w-8 h-8 animate-spin text-neon" />
     </div>

     <!-- Error State -->
     <div v-else-if="error" class="bg-red-500/10 border border-red-500 rounded-xl p-4 mb-6">
        <p class="text-red-500">{{ error }}</p>
        <button
          @click="loadPlan"
          class="mt-2 px-4 py-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 text-sm"
        >
          Повторить
        </button>
     </div>

     <!-- Plan Content -->
     <div v-else-if="plan">
        <!-- Progress Bar -->
        <div class="mb-6">
          <div class="flex justify-between text-sm text-gray-400 mb-2">
            <span>День {{ todayDayNumber + 1 }} из 30</span>
            <span>{{ progressPercentage }}%</span>
          </div>
          <div class="h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              class="h-full bg-neon transition-all duration-300"
              :style="{ width: `${progressPercentage}%` }"
            />
          </div>
        </div>

        <!-- Week Navigation -->
        <div class="flex items-center justify-between mb-4">
          <button
            @click="previousWeek"
            :disabled="!canGoToPreviousWeek"
            class="p-2 rounded-lg transition"
            :class="canGoToPreviousWeek ? 'bg-white/5 hover:bg-white/10' : 'opacity-30 cursor-not-allowed'"
          >
            <Icon icon="heroicons:chevron-left" class="w-5 h-5" />
          </button>

          <span class="text-sm font-medium">Неделя {{ currentWeek + 1 }} из 4</span>

          <button
            @click="nextWeek"
            :disabled="!canGoToNextWeek"
            class="p-2 rounded-lg transition"
            :class="canGoToNextWeek ? 'bg-white/5 hover:bg-white/10' : 'opacity-30 cursor-not-allowed'"
          >
            <Icon icon="heroicons:chevron-right" class="w-5 h-5" />
          </button>
        </div>

        <!-- Calendar Strip -->
        <div class="flex justify-between mb-8 bg-[#111] p-3 rounded-2xl">
          <div
            v-for="(d, i) in weekDays"
            :key="d.id"
            class="flex flex-col items-center gap-2"
          >
             <span class="text-xs text-gray-400">{{ d.dayName }}</span>
             <div
               class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all"
               :class="[
                  d.status === 'today' ? 'bg-neon text-black' :
                  d.status === 'done' ? 'bg-green-500/20 text-green-500' :
                  d.status === 'missed' ? 'bg-red-500/20 text-red-500' :
                  d.status === 'rest' ? 'bg-white/5 text-gray-500' :
                  'bg-transparent text-gray-600'
               ]"
             >
                <Icon v-if="d.status === 'done'" icon="heroicons:check" />
                <Icon v-else-if="d.status === 'missed'" icon="heroicons:x-mark" />
                <Icon v-else-if="d.status === 'rest'" icon="heroicons:moon" />
                <span v-else>{{ d.day_number + 1 }}</span>
             </div>
          </div>
        </div>

        <!-- Rest Day Message -->
        <div v-if="todayPlanDay?.is_rest_day" class="text-center py-12">
          <Icon icon="heroicons:moon" class="w-16 h-16 mx-auto mb-4 text-neon" />
          <h2 class="text-2xl font-bold mb-2">День отдыха</h2>
          <p class="text-gray-400">Восстановление - важная часть прогресса</p>
        </div>

        <!-- Today's Plan -->
        <div v-else class="mb-8">
          <SectionTitle
            title="Сегодня"
            :subtitle="`День ${todayDayNumber + 1}`"
          />

          <div v-if="todayExercises.length > 0" class="space-y-2">
              <ExerciseCard
                  v-for="ex in todayExercises"
                  :key="ex.name"
                  v-bind="ex"
              />
          </div>

          <div v-else class="text-center py-8 text-gray-400">
            Нет упражнений на сегодня
          </div>

          <button
            v-if="todayExercises.length > 0"
            @click="startTraining"
            class="w-full mt-6 py-4 rounded-xl bg-neon text-black font-bold flex items-center justify-center gap-2 hover:brightness-110 transition"
          >
              <Icon icon="heroicons:play" />
              Начать тренировку
          </button>
        </div>
     </div>

     <!-- No Plan State -->
     <div v-else class="text-center py-12">
        <Icon icon="heroicons:calendar" class="w-16 h-16 mx-auto mb-4 text-gray-600" />
        <h2 class="text-xl font-bold mb-2">Нет активного плана</h2>
        <p class="text-gray-400 mb-6">Создайте план тренировок</p>
        <button
          @click="handleRegeneratePlan"
          class="px-6 py-3 rounded-xl bg-neon text-black font-bold"
        >
          Создать план
        </button>
     </div>

     <!-- Regenerate Dialog -->
     <div
       v-if="showRegenerateDialog"
       class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 px-4"
       @click.self="showRegenerateDialog = false"
     >
        <div class="bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 max-w-sm w-full">
          <h3 class="text-xl font-bold mb-2">Создать новый план?</h3>
          <p class="text-gray-400 text-sm mb-6">
            Это деактивирует текущий план и создаст новый на основе вашего профиля.
          </p>

          <div class="flex gap-3">
            <button
              @click="showRegenerateDialog = false"
              :disabled="regenerating"
              class="flex-1 py-3 rounded-xl bg-white/5 hover:bg-white/10 font-medium transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Отмена
            </button>
            <button
              @click="handleRegeneratePlan"
              :disabled="regenerating"
              class="flex-1 py-3 rounded-xl bg-neon text-black font-bold hover:brightness-110 transition flex items-center justify-center gap-2 disabled:opacity-75 disabled:cursor-not-allowed"
            >
              <Icon
                v-if="regenerating"
                icon="heroicons:arrow-path"
                class="animate-spin"
              />
              <span v-if="regenerating">Генерация...</span>
              <span v-else>Создать</span>
            </button>
          </div>

          <!-- Progress hint during generation -->
          <div v-if="regenerating" class="mt-4 text-center">
            <p class="text-xs text-gray-500">
              Это может занять до 2 минут. Пожалуйста, подождите...
            </p>
          </div>
        </div>
     </div>
  </div>
</template>

<style scoped>
.bg-neon { background-color: var(--color-neon); }
</style>
