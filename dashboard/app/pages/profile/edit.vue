<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// Form state
const isSaving = ref(false)
const saveSuccess = ref(false)
const saveError = ref('')

// Profile data
const profile = ref({
  // Basic data
  full_name: '',
  age: null as number | null,
  gender: '',
  weight: null as number | null,
  height: null as number | null,

  // Body metrics
  target_weight: null as number | null,
  body_fat_percentage: null as number | null,

  // Fitness data
  fitness_goal: '',
  fitness_level: '',

  // Activity
  activity_level: '',
  weekly_workout_days: null as number | null,
  workout_duration_preference: null as number | null,

  // Health
  has_injuries: false,
  injury_details: '',
  medical_conditions: '',

  // Equipment
  has_equipment: false,
  available_equipment: ''
})

// Load current profile data
onMounted(() => {
  const user = authStore.user
  if (user) {
    profile.value.full_name = user.full_name || ''

    if (user.profile) {
      profile.value.age = user.profile.age
      profile.value.gender = user.profile.gender || ''
      profile.value.weight = user.profile.weight
      profile.value.height = user.profile.height
      profile.value.target_weight = user.profile.target_weight
      profile.value.body_fat_percentage = user.profile.body_fat_percentage
      profile.value.fitness_goal = user.profile.fitness_goal || ''
      profile.value.fitness_level = user.profile.fitness_level || ''
      profile.value.activity_level = user.profile.activity_level || ''
      profile.value.weekly_workout_days = user.profile.weekly_workout_days
      profile.value.workout_duration_preference = user.profile.workout_duration_preference
      profile.value.has_injuries = user.profile.has_injuries || false
      profile.value.injury_details = user.profile.injury_details || ''
      profile.value.medical_conditions = user.profile.medical_conditions || ''
      profile.value.has_equipment = user.profile.has_equipment || false
      profile.value.available_equipment = user.profile.available_equipment || ''
    }
  }
})

// Fitness goals options
const fitnessGoals = [
  { value: 'lose_weight', label: 'Похудеть' },
  { value: 'gain_muscle', label: 'Набрать мышечную массу' },
  { value: 'get_toned', label: 'Подтянуть тело' },
  { value: 'improve_endurance', label: 'Улучшить выносливость' },
  { value: 'maintain', label: 'Поддерживать форму' }
]

// Fitness levels
const fitnessLevels = [
  { value: 'beginner', label: 'Начинающий' },
  { value: 'intermediate', label: 'Средний' },
  { value: 'advanced', label: 'Продвинутый' }
]

// Activity levels
const activityLevels = [
  { value: 'sedentary', label: 'Малоподвижный' },
  { value: 'lightly_active', label: 'Легкая активность' },
  { value: 'moderately_active', label: 'Умеренная активность' },
  { value: 'very_active', label: 'Высокая активность' }
]

// Gender options
const genders = [
  { value: 'male', label: 'Мужской' },
  { value: 'female', label: 'Женский' },
  { value: 'other', label: 'Другой' }
]

// Weekly workout days options
const weeklyDaysOptions = [3, 4, 5, 6, 7]

// Workout duration options
const durationOptions = [
  { value: 15, label: '15 минут' },
  { value: 30, label: '30 минут' },
  { value: 45, label: '45 минут' },
  { value: 60, label: '60 минут' }
]

// BMI calculation
const bmi = computed(() => {
  if (profile.value.weight && profile.value.height) {
    const heightInMeters = profile.value.height / 100
    return (profile.value.weight / (heightInMeters * heightInMeters)).toFixed(1)
  }
  return null
})

// Save profile
const handleSave = async () => {
  isSaving.value = true
  saveError.value = ''
  saveSuccess.value = false

  try {
    // Prepare update data (only profile fields)
    const updateData: any = {
      age: profile.value.age,
      gender: profile.value.gender || null,
      weight: profile.value.weight,
      height: profile.value.height,
      target_weight: profile.value.target_weight,
      body_fat_percentage: profile.value.body_fat_percentage,
      fitness_goal: profile.value.fitness_goal || null,
      fitness_level: profile.value.fitness_level || null,
      activity_level: profile.value.activity_level || null,
      weekly_workout_days: profile.value.weekly_workout_days,
      workout_duration_preference: profile.value.workout_duration_preference,
      has_injuries: profile.value.has_injuries,
      injury_details: profile.value.injury_details || null,
      medical_conditions: profile.value.medical_conditions || null,
      has_equipment: profile.value.has_equipment,
      available_equipment: profile.value.available_equipment || null
    }

    // Update profile via auth store
    const success = await authStore.updateProfile(updateData)

    if (success) {
      saveSuccess.value = true
      setTimeout(() => {
        router.push('/profile')
      }, 1500)
    } else {
      saveError.value = 'Не удалось сохранить изменения'
    }
  } catch (error: any) {
    console.error('Save profile error:', error)
    saveError.value = error.message || 'Произошла ошибка при сохранении'
  } finally {
    isSaving.value = false
  }
}

// Cancel and go back
const handleCancel = () => {
  router.push('/profile')
}
</script>

<template>
  <div class="px-4 pt-12 pb-24">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <button @click="handleCancel" class="text-gray-400 hover:text-white">
        <Icon icon="heroicons:arrow-left" class="text-2xl" />
      </button>
      <h1 class="text-3xl font-bold">Личные данные</h1>
    </div>

    <!-- Success Message -->
    <div v-if="saveSuccess" class="bg-green-500/20 border border-green-500 text-green-500 px-4 py-3 rounded-xl mb-4">
      <div class="flex items-center gap-2">
        <Icon icon="heroicons:check-circle" class="text-xl" />
        <span>Данные успешно сохранены!</span>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="saveError" class="bg-red-500/20 border border-red-500 text-red-500 px-4 py-3 rounded-xl mb-4">
      <div class="flex items-center gap-2">
        <Icon icon="heroicons:exclamation-circle" class="text-xl" />
        <span>{{ saveError }}</span>
      </div>
    </div>

    <form @submit.prevent="handleSave" class="space-y-6">
      <!-- Basic Information -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:user" class="text-neon" />
          Основная информация
        </h2>

        <div class="space-y-4">
          <!-- Full Name -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Имя</label>
            <input
              v-model="profile.full_name"
              type="text"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
              placeholder="Ваше имя"
            />
          </div>

          <!-- Age -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Возраст</label>
            <input
              v-model.number="profile.age"
              type="number"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
              placeholder="Лет"
            />
          </div>

          <!-- Gender -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Пол</label>
            <select
              v-model="profile.gender"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            >
              <option value="">Выберите пол</option>
              <option v-for="gender in genders" :key="gender.value" :value="gender.value">
                {{ gender.label }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Body Metrics -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:chart-bar" class="text-neon" />
          Параметры тела
        </h2>

        <div class="space-y-4">
          <!-- Weight -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Текущий вес (кг)</label>
            <input
              v-model.number="profile.weight"
              type="number"
              step="0.1"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
              placeholder="70.0"
            />
          </div>

          <!-- Height -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Рост (см)</label>
            <input
              v-model.number="profile.height"
              type="number"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
              placeholder="175"
            />
          </div>

          <!-- BMI Display -->
          <div v-if="bmi" class="bg-neon/10 border border-neon/20 rounded-xl p-3">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-400">Индекс массы тела (ИМТ)</span>
              <span class="text-lg font-bold text-neon">{{ bmi }}</span>
            </div>
          </div>

          <!-- Target Weight -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Желаемый вес (кг) <span class="text-xs text-gray-500">(опционально)</span></label>
            <input
              v-model.number="profile.target_weight"
              type="number"
              step="0.1"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
              placeholder="65.0"
            />
          </div>

          <!-- Body Fat -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Процент жира в теле (%) <span class="text-xs text-gray-500">(опционально)</span></label>
            <input
              v-model.number="profile.body_fat_percentage"
              type="number"
              step="0.1"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
              placeholder="20.0"
            />
          </div>
        </div>
      </div>

      <!-- Fitness Goals -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:flag" class="text-neon" />
          Фитнес-цели
        </h2>

        <div class="space-y-4">
          <!-- Fitness Goal -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Основная цель</label>
            <select
              v-model="profile.fitness_goal"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            >
              <option value="">Выберите цель</option>
              <option v-for="goal in fitnessGoals" :key="goal.value" :value="goal.value">
                {{ goal.label }}
              </option>
            </select>
          </div>

          <!-- Fitness Level -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Уровень подготовки</label>
            <select
              v-model="profile.fitness_level"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            >
              <option value="">Выберите уровень</option>
              <option v-for="level in fitnessLevels" :key="level.value" :value="level.value">
                {{ level.label }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Activity & Schedule -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:calendar-days" class="text-neon" />
          Активность и расписание
        </h2>

        <div class="space-y-4">
          <!-- Activity Level -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Уровень повседневной активности</label>
            <select
              v-model="profile.activity_level"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            >
              <option value="">Выберите уровень</option>
              <option v-for="level in activityLevels" :key="level.value" :value="level.value">
                {{ level.label }}
              </option>
            </select>
          </div>

          <!-- Weekly Workout Days -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Тренировок в неделю</label>
            <select
              v-model.number="profile.weekly_workout_days"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            >
              <option :value="null">Выберите количество</option>
              <option v-for="days in weeklyDaysOptions" :key="days" :value="days">
                {{ days }} дней
              </option>
            </select>
          </div>

          <!-- Workout Duration -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Предпочтительная длительность тренировки</label>
            <select
              v-model.number="profile.workout_duration_preference"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            >
              <option :value="null">Выберите длительность</option>
              <option v-for="duration in durationOptions" :key="duration.value" :value="duration.value">
                {{ duration.label }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Health Considerations -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:heart" class="text-neon" />
          Здоровье
        </h2>

        <div class="space-y-4">
          <!-- Has Injuries -->
          <div class="flex items-center justify-between">
            <label class="text-sm text-gray-400">Есть травмы или ограничения</label>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="profile.has_injuries" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>

          <!-- Injury Details -->
          <div v-if="profile.has_injuries">
            <label class="block text-sm text-gray-400 mb-2">Описание травм</label>
            <textarea
              v-model="profile.injury_details"
              rows="3"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon resize-none"
              placeholder="Опишите травмы или ограничения..."
            ></textarea>
          </div>

          <!-- Medical Conditions -->
          <div>
            <label class="block text-sm text-gray-400 mb-2">Медицинские состояния <span class="text-xs text-gray-500">(если есть)</span></label>
            <textarea
              v-model="profile.medical_conditions"
              rows="3"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon resize-none"
              placeholder="Например: диабет, высокое давление..."
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Equipment -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:wrench-screwdriver" class="text-neon" />
          Оборудование
        </h2>

        <div class="space-y-4">
          <!-- Has Equipment -->
          <div class="flex items-center justify-between">
            <label class="text-sm text-gray-400">Есть доступ к оборудованию</label>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="profile.has_equipment" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>

          <!-- Available Equipment -->
          <div v-if="profile.has_equipment">
            <label class="block text-sm text-gray-400 mb-2">Доступное оборудование</label>
            <textarea
              v-model="profile.available_equipment"
              rows="3"
              class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon resize-none"
              placeholder="Например: гантели, коврик, резинки..."
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="flex gap-3">
        <button
          type="button"
          @click="handleCancel"
          class="flex-1 bg-[#1A1A1A] text-white py-4 rounded-xl font-semibold hover:bg-[#222] transition-colors"
        >
          Отмена
        </button>
        <button
          type="submit"
          :disabled="isSaving"
          class="flex-1 bg-neon text-black py-4 rounded-xl font-semibold hover:brightness-110 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <svg v-if="isSaving" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isSaving ? 'Сохранение...' : 'Сохранить' }}</span>
        </button>
      </div>
    </form>
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
