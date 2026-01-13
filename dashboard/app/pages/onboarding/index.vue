<script setup lang="ts">
import { Icon } from '@iconify/vue'
import confetti from 'canvas-confetti'
import FullScreenContainer from '~/components/ui/FullScreenContainer.vue'
import OnboardingStepHeader from '~/components/ui/OnboardingStepHeader.vue'
import SelectableCard from '~/components/ui/SelectableCard.vue'
import PrimaryButton from '~/components/ui/PrimaryButton.vue'
import { useOnboardingStore } from '~/stores/onboarding'

const store = useOnboardingStore()
const router = useRouter()

// Steps definition
type Step = 'welcome' | 'goal' | 'level' | 'gender' | 'physical-params' | 'how-it-works' | 'preparing' | 'success'
const currentStep = ref<Step>('welcome')
const isLoading = ref(false)

// Data for steps
const goals = [
  { id: 'lose-weight', title: 'Похудеть', icon: 'hugeicons:fire' },
  { id: 'tone-body', title: 'Привести тело в тонус', icon: 'hugeicons:body-armor' },
  { id: 'improve-fitness', title: 'Улучшить физическую форму', icon: 'hugeicons:favourite' }
]

const levels = [
  { id: 'beginner', title: 'Начальный', description: 'Только начинаю', icon: 'hugeicons:star' },
  { id: 'intermediate', title: 'Средний', description: 'Занимаюсь регулярно', icon: 'hugeicons:star-face' },
  { id: 'advanced', title: 'Продвинутый', description: 'Опытный спортсмен', icon: 'hugeicons:stars' }
]

const genders = [
  { id: 'male', title: 'Мужской', icon: 'hugeicons:user' },
  { id: 'female', title: 'Женский', icon: 'hugeicons:user-account' }
]

// Physical params state
const localHeight = ref<number | null>(store.height)
const localWeight = ref<number | null>(store.weight)
const localAge = ref<number | null>(store.age)

const howItWorksSteps = [
  { id: 1, title: 'Камера определяет положение тела', text: 'Используя технологию компьютерного зрения' },
  { id: 2, title: 'ИИ анализирует технику', text: 'Нейросеть оценивает правильность выполнения' },
  { id: 3, title: 'Приложение подсказывает, если форма нарушена', text: 'Получайте мгновенную обратную связь' }
]

// Navigation Logic
const nextStep = async (step: Step) => {
  currentStep.value = step
}

const handleWelcomeContinue = () => {
    nextStep('goal')
}

const handleGoalContinue = () => {
  if (store.goal) {
    nextStep('level')
  }
}

const handleLevelContinue = () => {
  if (store.level) {
    nextStep('gender')
  }
}

const handleGenderContinue = () => {
  if (store.gender) {
    nextStep('physical-params')
  }
}

const handlePhysicalParamsContinue = () => {
  if (localHeight.value && localWeight.value && localAge.value) {
    store.setPhysicalParams({
      height: localHeight.value,
      weight: localWeight.value,
      age: localAge.value
    })
    nextStep('how-it-works')
  }
}

const handleHowItWorksContinue = () => {
  nextStep('preparing')
  startPreparing()
}

const startPreparing = () => {
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
    nextStep('success')
    launchConfetti()
  }, 3000) // 3 seconds simulation
}

const handleSuccessContinue = () => {
  store.completeOnboarding()
  router.push('/home')
}

// Confetti Effect
const launchConfetti = () => {
  const duration = 3000
  const animationEnd = Date.now() + duration
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 }

  const randomInRange = (min: number, max: number) => Math.random() * (max - min) + min

  const interval: any = setInterval(function() {
    const timeLeft = animationEnd - Date.now()

    if (timeLeft <= 0) {
      return clearInterval(interval)
    }

    const particleCount = 50 * (timeLeft / duration)
    confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } })
    confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } })
  }, 250)
}

// Computed for header progress
const stepIndex = computed(() => {
  const map: Record<Step, number> = {
    'welcome': 1,
    'goal': 2,
    'level': 3,
    'gender': 4,
    'physical-params': 5,
    'how-it-works': 6,
    'preparing': 7,
    'success': 8
  }
  return map[currentStep.value]
})

const totalSteps = 8

// Computed for physical params validation
const isPhysicalParamsValid = computed(() => {
  return localHeight.value !== null &&
         localWeight.value !== null &&
         localAge.value !== null &&
         localHeight.value > 0 &&
         localWeight.value > 0 &&
         localAge.value > 0
})
</script>

<template>
  <FullScreenContainer>
    <OnboardingStepHeader
      v-if="['goal', 'level', 'gender', 'physical-params', 'how-it-works'].includes(currentStep)"
      :current-step="stepIndex - 1"
      :total-steps="5"
    />

    <transition name="fade" mode="out-in">
      
      <!-- STEP 1: WELCOME -->
      <div v-if="currentStep === 'welcome'" class="h-full flex flex-col pt-10">
         <div class="flex-1 flex flex-col items-center justify-center text-center relative">
             <!-- Background elements for visual flare -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-[#CCFF00] opacity-20 blur-[100px] rounded-full pointer-events-none" />
            
            <div class="relative z-10 mb-8">
               <!-- Image girl.png -->
               <img src="/girl.png" alt="Fitness Girl" class="h-[40vh] object-contain drop-shadow-2xl" />
            </div>

            <h1 class="text-3xl font-bold mb-4 px-4">Тренируйтесь правильно с помощью ИИ</h1>
            <p class="text-gray-400 px-4 max-w-md mx-auto">
              MuscleUp Vision анализирует технику упражнений через камеру и помогает выполнять тренировки безопасно и эффективно.
            </p>
         </div>
         <div class="mt-8 pb-8 px-4 w-full max-w-md mx-auto">
            <PrimaryButton @click="handleWelcomeContinue">
              Начать
            </PrimaryButton>
         </div>
      </div>

      <!-- STEP 2: GOAL -->
      <div v-else-if="currentStep === 'goal'" class="h-full flex flex-col pt-4">
          <div class="flex-1">
            <h1 class="text-3xl font-bold mb-2">Какая у вас цель?</h1>
            <p class="text-gray-400 mb-8">Выберите основную цель тренировок</p>
            
            <div class="space-y-4">
              <SelectableCard
                v-for="goal in goals"
                :key="goal.id"
                :title="goal.title"
                :icon="goal.icon"
                :selected="store.goal === goal.id"
                @click="store.setGoal(goal.id)"
              />
            </div>
          </div>
          <div class="mt-8 pb-8">
            <PrimaryButton 
              :disabled="!store.goal"
              icon="hugeicons:arrow-right-02"
              @click="handleGoalContinue"
            >
              Продолжить
            </PrimaryButton>
          </div>
      </div>

      <!-- STEP 3: LEVEL -->
      <div v-else-if="currentStep === 'level'" class="h-full flex flex-col pt-4">
        <div class="flex-1">
            <h1 class="text-3xl font-bold mb-2">Ваш уровень подготовки</h1>
            <p class="text-gray-400 mb-8">Это поможет подобрать оптимальную нагрузку</p>

            <div class="space-y-4">
              <SelectableCard
                v-for="level in levels"
                :key="level.id"
                :title="level.title"
                :description="level.description"
                :icon="level.icon"
                :selected="store.level === level.id"
                @click="store.setLevel(level.id)"
              />
            </div>
          </div>
          <div class="mt-8 pb-8">
            <PrimaryButton
              :disabled="!store.level"
              icon="hugeicons:arrow-right-02"
              @click="handleLevelContinue"
            >
              Продолжить
            </PrimaryButton>
          </div>
      </div>

      <!-- STEP 4: GENDER -->
      <div v-else-if="currentStep === 'gender'" class="h-full flex flex-col pt-4">
        <div class="flex-1">
            <h1 class="text-3xl font-bold mb-2">Ваш пол</h1>
            <p class="text-gray-400 mb-8">Это поможет подобрать программу тренировок</p>

            <div class="space-y-4">
              <SelectableCard
                v-for="gender in genders"
                :key="gender.id"
                :title="gender.title"
                :icon="gender.icon"
                :selected="store.gender === gender.id"
                @click="store.setGender(gender.id)"
              />
            </div>
          </div>
          <div class="mt-8 pb-8">
            <PrimaryButton
              :disabled="!store.gender"
              icon="hugeicons:arrow-right-02"
              @click="handleGenderContinue"
            >
              Продолжить
            </PrimaryButton>
          </div>
      </div>

      <!-- STEP 5: PHYSICAL PARAMS -->
      <div v-else-if="currentStep === 'physical-params'" class="h-full flex flex-col pt-4">
        <div class="flex-1">
            <h1 class="text-3xl font-bold mb-2">Ваши параметры</h1>
            <p class="text-gray-400 mb-8">Для точного подбора нагрузки и калорий</p>

            <div class="space-y-6">
              <!-- Height -->
              <div class="bg-[#1A1A1A] rounded-2xl p-5">
                <label class="block text-sm text-gray-400 mb-3">Рост (см)</label>
                <div class="flex items-center gap-3">
                  <Icon icon="hugeicons:arrow-up-down" class="text-[#CCFF00] text-xl" />
                  <input
                    v-model.number="localHeight"
                    type="number"
                    placeholder="170"
                    class="flex-1 bg-transparent text-white text-2xl font-bold outline-none"
                    min="100"
                    max="250"
                  />
                  <span class="text-gray-500 text-sm">см</span>
                </div>
              </div>

              <!-- Weight -->
              <div class="bg-[#1A1A1A] rounded-2xl p-5">
                <label class="block text-sm text-gray-400 mb-3">Вес (кг)</label>
                <div class="flex items-center gap-3">
                  <Icon icon="hugeicons:scale" class="text-[#CCFF00] text-xl" />
                  <input
                    v-model.number="localWeight"
                    type="number"
                    placeholder="70"
                    class="flex-1 bg-transparent text-white text-2xl font-bold outline-none"
                    min="30"
                    max="200"
                  />
                  <span class="text-gray-500 text-sm">кг</span>
                </div>
              </div>

              <!-- Age -->
              <div class="bg-[#1A1A1A] rounded-2xl p-5">
                <label class="block text-sm text-gray-400 mb-3">Возраст (лет)</label>
                <div class="flex items-center gap-3">
                  <Icon icon="hugeicons:calendar-01" class="text-[#CCFF00] text-xl" />
                  <input
                    v-model.number="localAge"
                    type="number"
                    placeholder="25"
                    class="flex-1 bg-transparent text-white text-2xl font-bold outline-none"
                    min="10"
                    max="100"
                  />
                  <span class="text-gray-500 text-sm">лет</span>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-8 pb-8">
            <PrimaryButton
              :disabled="!isPhysicalParamsValid"
              icon="hugeicons:arrow-right-02"
              @click="handlePhysicalParamsContinue"
            >
              Продолжить
            </PrimaryButton>
          </div>
      </div>

      <!-- STEP 6: HOW IT WORKS -->
      <div v-else-if="currentStep === 'how-it-works'" class="h-full flex flex-col pt-4">
         <div class="flex-1">
            <h1 class="text-3xl font-bold mb-2">Как работает MuscleUp Vision</h1>
            <p class="text-gray-400 mb-8">Технология компьютерного зрения для идеальной техники</p>

            <div class="space-y-6">
              <div
                v-for="step in howItWorksSteps"
                :key="step.id"
                class="flex items-start gap-4 p-4 bg-[#1A1A1A] rounded-2xl"
              >
                <div class="w-10 h-10 rounded-xl bg-[#CCFF00] flex items-center justify-center text-black font-bold text-xl shrink-0">
                  {{ step.id }}
                </div>
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <h3 class="font-bold">{{ step.title }}</h3>
                  </div>
                  <p class="text-sm text-gray-400">{{ step.text }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-8 pb-8">
            <PrimaryButton
              icon="hugeicons:arrow-right-02"
              @click="handleHowItWorksContinue"
            >
              Продолжить
            </PrimaryButton>
          </div>
      </div>

      <!-- STEP 7: PREPARING -->
      <div v-else-if="currentStep === 'preparing'" class="flex-1 w-full flex flex-col items-center justify-center text-center">
         <div class="relative w-32 h-32 mb-8 items-center justify-center flex">
             <!-- Spinner Ring -->
             <div class="absolute inset-0 border-4 border-[#1A1A1A] rounded-full"></div>
             <div class="absolute inset-0 border-4 border-[#CCFF00] rounded-full animate-spin border-t-transparent"></div>
             <Icon icon="hugeicons:ai-brain-01" class="text-5xl text-[#CCFF00]" />
         </div>
         <h2 class="text-2xl font-bold mb-2">Формируем ваш план тренировок</h2>
         <p class="text-gray-400 mb-8">План создаётся на основе ваших целей и уровня подготовки</p>
      </div>

      <!-- STEP 8: SUCCESS -->
      <div v-else-if="currentStep === 'success'" class="flex-1 w-full flex flex-col items-center justify-center text-center">
         <div class="w-24 h-24 bg-[#CCFF00] rounded-full flex items-center justify-center mb-8 shadow-[0_0_40px_rgba(204,255,0,0.3)]">
             <Icon icon="hugeicons:tick-02" class="text-5xl text-black" />
         </div>
         
         <h1 class="text-3xl font-bold mb-2">Ваш план готов</h1>
         <p class="text-gray-400 mb-12 max-w-xs mx-auto">Начните первую тренировку и отслеживайте прогресс каждый день.</p>

         <div class="w-full space-y-4 max-w-md mx-auto px-4 pb-8">
             <PrimaryButton 
                @click="handleSuccessContinue"
             >
                Начать тренировку
             </PrimaryButton>
             
             <button @click="handleSuccessContinue" class="w-full py-4 rounded-xl border border-[#333] text-white font-medium hover:bg-[#1A1A1A] transition-colors">
                Посмотреть план
             </button>
         </div>
      </div>

    </transition>
  </FullScreenContainer>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
