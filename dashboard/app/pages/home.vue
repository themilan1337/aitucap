<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ref, computed, onMounted } from 'vue'
import SectionTitle from '~/components/SectionTitle.vue'
import ExerciseCard from '~/components/ExerciseCard.vue'
import StatCard from '~/components/StatCard.vue'
import type { WorkoutPlan, PlanDay } from '~/composables/usePlan'
import type { WorkoutSession } from '~/composables/useWorkouts'
import type { Achievement } from '~/composables/useAchievements'

// State
const plan = ref<WorkoutPlan | null>(null)
const workouts = ref<WorkoutSession[]>([])
const achievements = ref<Achievement[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

// Get composables
const { fetchActivePlan } = usePlan()
const { fetchHistory } = useWorkouts()
const { fetchAchievements } = useAchievements()

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
 * Calculate streak from workout history
 */
const streak = computed(() => {
  if (workouts.value.length === 0) return 0

  // Get unique workout dates (YYYY-MM-DD format)
  const workoutDates = Array.from(
    new Set(
      workouts.value.map(w => {
        const date = new Date(w.completed_at)
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
      })
    )
  ).sort().reverse()

  if (workoutDates.length === 0) return 0

  // Check if most recent workout was today or yesterday
  const today = new Date()
  const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  const yesterdayStr = `${yesterday.getFullYear()}-${String(yesterday.getMonth() + 1).padStart(2, '0')}-${String(yesterday.getDate()).padStart(2, '0')}`

  if (workoutDates[0] !== todayStr && workoutDates[0] !== yesterdayStr) {
    // Streak is broken
    return 0
  }

  // Count consecutive days
  let streakCount = 1
  let currentDate = new Date(workoutDates[0])

  for (let i = 1; i < workoutDates.length; i++) {
    const expectedDate = new Date(currentDate)
    expectedDate.setDate(expectedDate.getDate() - 1)
    const expectedStr = `${expectedDate.getFullYear()}-${String(expectedDate.getMonth() + 1).padStart(2, '0')}-${String(expectedDate.getDate()).padStart(2, '0')}`

    if (workoutDates[i] === expectedStr) {
      streakCount++
      currentDate = expectedDate
    } else {
      break
    }
  }

  return streakCount
})

/**
 * Get today's plan day
 */
const todayPlanDay = computed(() => {
  if (!plan.value || !plan.value.days) return null

  const startDate = new Date(plan.value.week_start_date)
  const today = new Date()
  const diffTime = today.getTime() - startDate.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  const dayNumber = Math.max(0, Math.min(29, diffDays))

  return plan.value.days.find(d => d.day_number === dayNumber)
})

/**
 * Get today's exercises
 */
const todayExercises = computed(() => {
  if (!todayPlanDay.value || todayPlanDay.value.is_rest_day) return []

  return todayPlanDay.value.exercises.map(ex => ({
    id: ex.id,
    name: exerciseNames[ex.exercise_type] || ex.exercise_type,
    sets: ex.target_sets,
    reps: ex.target_reps
  }))
})

/**
 * Calculate this week's stats
 */
const weeklyStats = computed(() => {
  const oneWeekAgo = new Date()
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)

  const weekWorkouts = workouts.value.filter(w => {
    const workoutDate = new Date(w.completed_at)
    return workoutDate >= oneWeekAgo
  })

  const totalWorkouts = weekWorkouts.length
  const totalCalories = weekWorkouts.reduce((sum, w) => sum + (w.total_calories || 0), 0)

  return {
    workouts: totalWorkouts,
    calories: Math.round(totalCalories)
  }
})

/**
 * Calculate lifetime stats
 */
const lifetimeStats = computed(() => {
  const totalWorkouts = workouts.value.length
  const totalReps = workouts.value.reduce((sum, workout) => {
    const workoutReps = workout.exercises?.reduce((exSum, ex) => exSum + (ex.reps || 0), 0) || 0
    return sum + workoutReps
  }, 0)

  return {
    totalWorkouts,
    totalReps
  }
})

/**
 * Unlocked achievements count
 */
const unlockedAchievementsCount = computed(() => {
  return achievements.value.filter(a => a.unlocked_at !== null).length
})

/**
 * Load all data on mount
 */
const loadData = async () => {
  try {
    loading.value = true
    error.value = null

    // Fetch all data in parallel
    const [planData, workoutsData, achievementsData] = await Promise.all([
      fetchActivePlan().catch(() => null), // Don't fail if no plan
      fetchHistory(30), // Get last 30 workouts for accurate streak
      fetchAchievements().catch(() => []) // Don't fail if no achievements
    ])

    plan.value = planData
    workouts.value = workoutsData
    achievements.value = achievementsData
  } catch (err: any) {
    console.error('Failed to load home data:', err)
    error.value = err.message || 'Не удалось загрузить данные'
  } finally {
    loading.value = false
  }
}

/**
 * Start training
 */
const startTraining = () => {
  if (!todayPlanDay.value || todayPlanDay.value.is_rest_day) {
    navigateTo('/train')
    return
  }

  navigateTo({
    path: '/train',
    query: {
      plan_day_id: todayPlanDay.value.id
    }
  })
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="px-4 pt-12 pb-8">
     <header class="flex justify-between items-start mb-6">
        <div>
           <p class="text-gray-400 text-sm mb-1">Добро пожаловать!</p>
           <h1 class="text-3xl font-bold">Время тренироваться</h1>
        </div>
        <button
          @click="loadData"
          class="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition"
        >
          <Icon icon="heroicons:arrow-path" class="w-5 h-5" :class="{ 'animate-spin': loading }" />
        </button>
     </header>

     <!-- Loading State -->
     <div v-if="loading" class="flex items-center justify-center py-20">
        <Icon icon="heroicons:arrow-path" class="w-8 h-8 animate-spin text-neon" />
     </div>

     <!-- Error State -->
     <div v-else-if="error" class="bg-red-500/10 border border-red-500 rounded-xl p-4 mb-6">
        <p class="text-red-500">{{ error }}</p>
        <button
          @click="loadData"
          class="mt-2 px-4 py-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 text-sm"
        >
          Повторить
        </button>
     </div>

     <!-- Content -->
     <div v-else>
        <!-- Streak Card -->
        <div class="w-full bg-[#111] rounded-2xl p-4 flex items-center gap-4 mb-8">
          <div class="w-12 h-12 rounded-full bg-neon/10 flex items-center justify-center text-neon">
             <Icon icon="heroicons:fire" class="text-2xl" />
          </div>
          <div>
             <h2 class="text-xl font-bold text-white">
                <span class="text-neon">{{ streak }}</span> {{ streak === 1 ? 'день' : streak < 5 ? 'дня' : 'дней' }} подряд!
             </h2>
             <p class="text-xs text-gray-400">
                {{ streak === 0 ? 'Начните тренировку сегодня' : 'Продолжайте в том же духе' }}
             </p>
          </div>
        </div>

        <!-- Today's Training -->
        <div class="mb-8">
          <SectionTitle title="Сегодняшняя тренировка" />

          <!-- Rest Day -->
          <div v-if="todayPlanDay?.is_rest_day" class="bg-[#111] rounded-3xl p-8 text-center">
            <Icon icon="heroicons:moon" class="w-12 h-12 mx-auto mb-4 text-neon" />
            <h3 class="text-xl font-bold mb-2">День отдыха</h3>
            <p class="text-gray-400 text-sm">Восстановление - важная часть прогресса</p>
          </div>

          <!-- Training Day -->
          <div v-else-if="todayExercises.length > 0" class="bg-[#111] rounded-3xl p-5">
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
                   <span>~{{ todayExercises.length * 5 }} мин</span>
                </div>
                <div class="flex items-center gap-2">
                    <Icon icon="heroicons:fire" class="text-neon" />
                    <span>{{ todayExercises.length }} упр.</span>
                </div>
             </div>

             <!-- CTA -->
             <button
               @click="startTraining"
               class="w-full py-4 rounded-xl bg-neon text-black font-bold text-lg flex items-center justify-center gap-2 hover:brightness-110 active:scale-[0.98] transition-all"
             >
                <Icon icon="heroicons:play" />
                Начать тренировку
             </button>
          </div>

          <!-- No Plan -->
          <div v-else class="bg-[#111] rounded-3xl p-8 text-center">
            <Icon icon="heroicons:calendar" class="w-12 h-12 mx-auto mb-4 text-gray-600" />
            <h3 class="text-xl font-bold mb-2">Нет плана</h3>
            <p class="text-gray-400 text-sm mb-4">Создайте план тренировок</p>
            <router-link
              to="/plan"
              class="inline-block px-6 py-3 rounded-xl bg-neon text-black font-bold hover:brightness-110 transition"
            >
              Перейти к плану
            </router-link>
          </div>
        </div>

        <!-- Weekly Summary -->
        <div class="mb-8">
          <SectionTitle
            title="Эта неделя"
            :right-text="`${weeklyStats.workouts} из 7 дней`"
          />
          <div class="grid grid-cols-2 gap-4">
             <StatCard
               label="Тренировок"
               :value="weeklyStats.workouts"
               icon="heroicons:view-columns"
               icon-color="text-neon"
             />
             <StatCard
               label="Калорий"
               :value="weeklyStats.calories"
               icon="heroicons:fire"
               icon-color="text-neon"
             />
          </div>
        </div>

        <!-- Lifetime Stats -->
        <div class="mb-8">
          <router-link to="/progress" class="block">
            <SectionTitle title="Общая статистика" right-text="Подробнее →" />
          </router-link>
          <div class="grid grid-cols-2 gap-4">
             <StatCard
               label="Всего тренировок"
               :value="lifetimeStats.totalWorkouts"
               icon="heroicons:check-circle"
             />
             <StatCard
               label="Всего повторений"
               :value="lifetimeStats.totalReps"
               icon="heroicons:arrow-path"
             />
          </div>
        </div>

        <!-- Achievements Teaser -->
        <div v-if="achievements.length > 0">
          <router-link to="/progress" class="block">
            <SectionTitle
              title="Достижения"
              :right-text="`${unlockedAchievementsCount} / ${achievements.length}`"
            />
          </router-link>
          <div class="flex gap-3 overflow-x-auto pb-2">
            <div
              v-for="achievement in achievements.slice(0, 4)"
              :key="achievement.id"
              class="flex-shrink-0 w-20 h-20 rounded-xl flex items-center justify-center text-2xl transition"
              :class="achievement.unlocked_at ? 'bg-neon/20' : 'bg-white/5 grayscale opacity-50'"
            >
              <Icon :icon="`heroicons:${achievement.icon}`" />
            </div>
          </div>
        </div>
     </div>
  </div>
</template>

<style scoped>
.text-neon {
    color: var(--color-neon);
}
.bg-neon {
    background-color: var(--color-neon);
}
</style>
