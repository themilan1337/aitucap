<script setup lang="ts">
import { useTrainingStore } from '~/stores/training'
import { Icon } from '@iconify/vue'
import SectionTitle from '~/components/SectionTitle.vue'
import ExerciseCard from '~/components/ExerciseCard.vue'
import StatCard from '~/components/StatCard.vue'
import PrimaryButton from '~/components/ui/PrimaryButton.vue' // Re-using if compatible, or just standard button

const store = useTrainingStore()

// Mock data helpers
const todayDuration = 15 // min
const muscleGroupTarget = "Ноги"

</script>

<template>
  <div class="px-4 pt-12 pb-8">
     <header class="flex justify-between items-start mb-6">
        <div>
           <p class="text-gray-400 text-sm mb-1">Добро пожаловать!</p>
           <h1 class="text-3xl font-bold">Время тренироваться</h1>
        </div>
     </header>

     <div class="w-full bg-[#111] rounded-2xl p-4 flex items-center gap-4 mb-8">
        <div class="w-12 h-12 rounded-full bg-neon/10 flex items-center justify-center text-neon">
           <Icon icon="heroicons:fire" class="text-2xl" />
        </div>
        <div>
           <h2 class="text-xl font-bold text-white">
              <span class="text-neon">{{ store.streak }}</span> дней подряд!
           </h2>
           <p class="text-xs text-gray-400">Продолжайте в том же духе</p>
        </div>
     </div>

     <!-- Today's Training -->
     <div class="mb-8">
        <SectionTitle title="Сегодняшняя тренировка" />
        
        <div class="bg-[#111] rounded-3xl p-5">
           <!-- Exercises List -->
           <div class="mb-4 border border-white/5 rounded-xl">
              <ExerciseCard 
                 v-for="exercise in store.todayExercises"
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
                 <span>{{ todayDuration }} мин</span>
              </div>
              <div class="flex items-center gap-2">
                  <Icon icon="heroicons:stop" class="text-neon" />
                  <span>{{ muscleGroupTarget }}</span>
              </div>
           </div>

           <!-- CTA -->
           <button class="w-full py-4 rounded-xl bg-neon text-black font-bold text-lg flex items-center justify-center gap-2 hover:brightness-110 active:scale-[0.98] transition-all">
              Начать тренировку
           </button>
        </div>
     </div>

     <!-- Weekly Summary -->
     <div class="mb-8">
        <SectionTitle title="Эта неделя" right-text="6 из 7 дней" />
        <div class="grid grid-cols-2 gap-4">
           <StatCard 
             label="Тренировок" 
             :value="store.weeklyStats.workouts"
             icon="heroicons:view-columns"
             icon-color="text-neon"
           />
           <StatCard 
             label="Калорий" 
             :value="store.weeklyStats.calories"
             icon="heroicons:fire"
             icon-color="text-neon"
           />
        </div>
     </div>
     
     <!-- Lifetime/General Stats Teaser -->
      <div>
        <SectionTitle title="Общая статистика" />
        <div class="grid grid-cols-2 gap-4">
           <StatCard 
             label="Всего тренировок" 
             :value="store.lifetimeStats.totalWorkouts"
             icon="heroicons:check-circle"
           />
           <StatCard 
             label="Всего повторений" 
             :value="store.lifetimeStats.totalReps"
             icon="heroicons:arrow-path" 
           />
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
