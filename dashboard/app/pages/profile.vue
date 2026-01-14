<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { computed, ref } from 'vue'
import AchievementCard from '~/components/AchievementCard.vue'
import WorkoutHistoryCard from '~/components/WorkoutHistoryCard.vue'
import { useTrainingStore } from '~/stores/training'
import { useAuthStore } from '~/stores/auth'

const store = useTrainingStore()
const authStore = useAuthStore()

const isLoggingOut = ref(false)

const unlockedAchievements = computed(() =>
  store.achievements.filter(a => a.unlocked).length
)

// Get user display name and avatar from auth store
const userDisplayName = computed(() => authStore.userName)
const userAvatar = computed(() => authStore.userAvatar)
const userEmail = computed(() => authStore.user?.email || '')

// Format join date
const joinDate = computed(() => {
  if (!authStore.user?.created_at) return 'января 2025'
  const date = new Date(authStore.user.created_at)
  const months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                   'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
  return `${months[date.getMonth()]} ${date.getFullYear()}`
})

/**
 * Logout from current device
 */
const handleLogout = async () => {
  if (isLoggingOut.value) return

  isLoggingOut.value = true

  try {
    await authStore.logout()
    // authStore.logout() already redirects to /login
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    isLoggingOut.value = false
  }
}

/**
 * Logout from all devices
 */
const handleLogoutAll = async () => {
  if (isLoggingOut.value) return

  if (!confirm('Вы уверены, что хотите выйти со всех устройств?')) {
    return
  }

  isLoggingOut.value = true

  try {
    await authStore.logoutAllDevices()
    // authStore.logoutAllDevices() already redirects to /login
  } catch (error) {
    console.error('Logout all devices error:', error)
  } finally {
    isLoggingOut.value = false
  }
}
</script>

<template>
  <div class="px-4 pt-12 pb-24">
    <h1 class="text-3xl font-bold mb-6">Профиль</h1>

    <!-- Profile Header -->
    <div class="flex flex-col items-center mb-6">
      <!-- User Avatar -->
      <div v-if="userAvatar" class="w-32 h-32 rounded-full mb-4 overflow-hidden ring-2 ring-neon/20">
        <img :src="userAvatar" :alt="userDisplayName" class="w-full h-full object-cover" />
      </div>
      <div v-else class="w-32 h-32 rounded-full bg-[#424700] flex items-center justify-center text-neon mb-4">
        <Icon icon="heroicons:user" class="text-6xl" />
      </div>

      <!-- User Info -->
      <h2 class="text-2xl font-bold mb-1">{{ userDisplayName }}</h2>
      <p class="text-gray-400 text-sm mb-1">{{ userEmail }}</p>
      <p class="text-gray-500 text-xs mb-4">С нами с {{ joinDate }}</p>

      <button class="px-8 py-3 bg-neon text-black font-semibold rounded-xl hover:brightness-110 transition-all">
        Редактировать профиль
      </button>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-3 gap-4 mb-8 bg-[#1A1A1A] rounded-2xl p-4">
      <div class="flex flex-col items-center">
        <span class="text-3xl font-bold text-neon">{{ store.lifetimeStats.totalWorkouts }}</span>
        <span class="text-xs text-gray-400 mt-1">Тренировок</span>
      </div>
      <div class="flex flex-col items-center">
        <span class="text-3xl font-bold text-neon">{{ store.lifetimeStats.totalReps }}</span>
        <span class="text-xs text-gray-400 mt-1">Повторений</span>
      </div>
      <div class="flex flex-col items-center">
        <span class="text-3xl font-bold text-neon">{{ store.lifetimeStats.avgAccuracy }}%</span>
        <span class="text-xs text-gray-400 mt-1">Точность</span>
      </div>
    </div>

    <!-- Achievements Section -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-2">
          <Icon icon="heroicons:trophy" class="text-neon text-xl" />
          <h3 class="text-lg font-semibold">Достижения</h3>
        </div>
        <span class="text-sm text-gray-400">{{ unlockedAchievements }}/{{ store.achievements.length }}</span>
      </div>

      <div class="grid grid-cols-3 gap-4">
        <AchievementCard
          v-for="achievement in store.achievements"
          :key="achievement.id"
          :name="achievement.name"
          :icon="achievement.icon"
          :unlocked="achievement.unlocked"
        />
      </div>
    </div>

    <!-- Recent Workouts Section -->
    <div class="mb-8">
      <div class="flex items-center gap-2 mb-4">
        <Icon icon="heroicons:clock" class="text-neon text-xl" />
        <h3 class="text-lg font-semibold">Последние тренировки</h3>
      </div>

      <WorkoutHistoryCard
        v-for="(workout, index) in store.workoutHistory"
        :key="index"
        :workout="workout"
      />
    </div>

    <!-- Settings Menu -->
    <div class="bg-[#1A1A1A] rounded-2xl overflow-hidden mb-4">
      <button class="w-full flex items-center justify-between p-4 hover:bg-[#222] transition-colors border-b border-white/5">
        <div class="flex items-center gap-3">
          <Icon icon="heroicons:user-circle" class="text-neon text-xl" />
          <span class="text-white">Личные данные</span>
        </div>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>

      <button class="w-full flex items-center justify-between p-4 hover:bg-[#222] transition-colors border-b border-white/5">
        <div class="flex items-center gap-3">
          <Icon icon="heroicons:bell" class="text-neon text-xl" />
          <span class="text-white">Уведомления</span>
        </div>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>

      <button class="w-full flex items-center justify-between p-4 hover:bg-[#222] transition-colors border-b border-white/5">
        <div class="flex items-center gap-3">
          <Icon icon="heroicons:camera" class="text-neon text-xl" />
          <span class="text-white">Настройки камеры</span>
        </div>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>

      <button class="w-full flex items-center justify-between p-4 hover:bg-[#222] transition-colors border-b border-white/5">
        <div class="flex items-center gap-3">
          <Icon icon="heroicons:globe-alt" class="text-neon text-xl" />
          <span class="text-white">Язык</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-gray-400 text-sm">Русский</span>
          <Icon icon="heroicons:chevron-right" class="text-gray-500" />
        </div>
      </button>

      <button class="w-full flex items-center justify-between p-4 hover:bg-[#222] transition-colors border-b border-white/5">
        <div class="flex items-center gap-3">
          <Icon icon="heroicons:question-mark-circle" class="text-neon text-xl" />
          <span class="text-white">Помощь и поддержка</span>
        </div>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>

      <button class="w-full flex items-center justify-between p-4 hover:bg-[#222] transition-colors">
        <div class="flex items-center gap-3">
          <Icon icon="heroicons:information-circle" class="text-neon text-xl" />
          <span class="text-white">О приложении</span>
        </div>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>
    </div>

    <!-- Logout Section -->
    <div class="space-y-3 mb-4">
      <!-- Logout Button -->
      <button
        @click="handleLogout"
        :disabled="isLoggingOut"
        class="w-full bg-[#1A1A1A] text-red-500 py-4 rounded-2xl flex items-center justify-center gap-2 hover:bg-[#222] transition-colors disabled:opacity-50"
      >
        <Icon v-if="!isLoggingOut" icon="heroicons:arrow-left-on-rectangle" class="text-xl" />
        <svg v-else class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="font-semibold">{{ isLoggingOut ? 'Выход...' : 'Выйти' }}</span>
      </button>

      <!-- Logout from All Devices Button -->
      <button
        @click="handleLogoutAll"
        :disabled="isLoggingOut"
        class="w-full bg-[#1A1A1A] text-orange-500 py-4 rounded-2xl flex items-center justify-center gap-2 hover:bg-[#222] transition-colors disabled:opacity-50"
      >
        <Icon icon="heroicons:device-phone-mobile" class="text-xl" />
        <span class="font-semibold">Выйти со всех устройств</span>
      </button>
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
