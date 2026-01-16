<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Camera settings
const settings = ref({
  cameraPosition: 'front', // 'front' | 'back'
  showGrid: true,
  showSkeleton: true,
  showKeypoints: false,
  confidenceThreshold: 0.7,
  showFeedback: true,
  voiceGuidance: false,
  mirrorMode: true
})

const isSaving = ref(false)

// Confidence threshold options
const confidenceOptions = [
  { value: 0.5, label: 'Низкий (50%)' },
  { value: 0.6, label: 'Средний (60%)' },
  { value: 0.7, label: 'Высокий (70%)' },
  { value: 0.8, label: 'Очень высокий (80%)' }
]

// Save settings
const handleSave = () => {
  isSaving.value = true

  // Save to localStorage
  localStorage.setItem('cameraSettings', JSON.stringify(settings.value))

  setTimeout(() => {
    isSaving.value = false
    router.push('/profile')
  }, 500)
}

// Load settings from localStorage
const loadSettings = () => {
  const saved = localStorage.getItem('cameraSettings')
  if (saved) {
    try {
      settings.value = JSON.parse(saved)
    } catch (error) {
      console.error('Failed to load camera settings:', error)
    }
  }
}

// Reset to defaults
const handleReset = () => {
  settings.value = {
    cameraPosition: 'front',
    showGrid: true,
    showSkeleton: true,
    showKeypoints: false,
    confidenceThreshold: 0.7,
    showFeedback: true,
    voiceGuidance: false,
    mirrorMode: true
  }
}

// Load on mount
loadSettings()
</script>

<template>
  <div class="px-4 pt-12 pb-24">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <button @click="router.push('/profile')" class="text-gray-400 hover:text-white">
        <Icon icon="heroicons:arrow-left" class="text-2xl" />
      </button>
      <h1 class="text-3xl font-bold">Настройки камеры</h1>
    </div>

    <div class="space-y-6">
      <!-- Camera Position -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:camera" class="text-neon" />
          Положение камеры
        </h2>

        <div class="space-y-3">
          <label class="flex items-center justify-between p-3 bg-[#111] rounded-xl cursor-pointer hover:bg-[#181818] transition-colors">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:device-phone-mobile" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Фронтальная камера</div>
                <div class="text-sm text-gray-400">Для селфи режима</div>
              </div>
            </div>
            <input
              type="radio"
              v-model="settings.cameraPosition"
              value="front"
              class="w-5 h-5 accent-neon"
            />
          </label>

          <label class="flex items-center justify-between p-3 bg-[#111] rounded-xl cursor-pointer hover:bg-[#181818] transition-colors">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:camera" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Задняя камера</div>
                <div class="text-sm text-gray-400">Для съемки с другого угла</div>
              </div>
            </div>
            <input
              type="radio"
              v-model="settings.cameraPosition"
              value="back"
              class="w-5 h-5 accent-neon"
            />
          </label>
        </div>
      </div>

      <!-- Visual Aids -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:eye" class="text-neon" />
          Визуальные подсказки
        </h2>

        <div class="space-y-4">
          <!-- Show Grid -->
          <div class="flex items-center justify-between p-3 bg-[#111] rounded-xl">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:squares-2x2" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Показывать сетку</div>
                <div class="text-sm text-gray-400">Помогает с позиционированием</div>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.showGrid" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>

          <!-- Show Skeleton -->
          <div class="flex items-center justify-between p-3 bg-[#111] rounded-xl">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:user" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Показывать скелет</div>
                <div class="text-sm text-gray-400">Визуализация позы тела</div>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.showSkeleton" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>

          <!-- Show Keypoints -->
          <div class="flex items-center justify-between p-3 bg-[#111] rounded-xl">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:map-pin" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Показывать ключевые точки</div>
                <div class="text-sm text-gray-400">Точки суставов и тела</div>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.showKeypoints" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>

          <!-- Mirror Mode -->
          <div class="flex items-center justify-between p-3 bg-[#111] rounded-xl">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:arrows-right-left" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Зеркальный режим</div>
                <div class="text-sm text-gray-400">Отражать изображение</div>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.mirrorMode" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Detection Settings -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:adjustments-horizontal" class="text-neon" />
          Настройки распознавания
        </h2>

        <div class="space-y-4">
          <!-- Confidence Threshold -->
          <div>
            <label class="block text-sm text-gray-400 mb-3">Порог уверенности</label>
            <div class="space-y-2">
              <label
                v-for="option in confidenceOptions"
                :key="option.value"
                class="flex items-center justify-between p-3 bg-[#111] rounded-xl cursor-pointer hover:bg-[#181818] transition-colors"
              >
                <span class="font-medium">{{ option.label }}</span>
                <input
                  type="radio"
                  v-model.number="settings.confidenceThreshold"
                  :value="option.value"
                  class="w-5 h-5 accent-neon"
                />
              </label>
            </div>
            <p class="text-xs text-gray-500 mt-2">
              Чем выше порог, тем точнее должна быть поза для засчитывания повторения
            </p>
          </div>
        </div>
      </div>

      <!-- Feedback Settings -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:speaker-wave" class="text-neon" />
          Обратная связь
        </h2>

        <div class="space-y-4">
          <!-- Show Feedback -->
          <div class="flex items-center justify-between p-3 bg-[#111] rounded-xl">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:chat-bubble-bottom-center-text" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Показывать подсказки</div>
                <div class="text-sm text-gray-400">Советы по технике выполнения</div>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.showFeedback" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>

          <!-- Voice Guidance -->
          <div class="flex items-center justify-between p-3 bg-[#111] rounded-xl">
            <div class="flex items-center gap-3">
              <Icon icon="heroicons:megaphone" class="text-neon text-xl" />
              <div>
                <div class="font-medium">Голосовое сопровождение</div>
                <div class="text-sm text-gray-400">Звуковые инструкции (скоро)</div>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer opacity-50">
              <input type="checkbox" v-model="settings.voiceGuidance" class="sr-only peer" disabled>
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-neon"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3">
        <button
          @click="handleReset"
          class="flex-1 bg-[#1A1A1A] text-white py-4 rounded-xl font-semibold hover:bg-[#222] transition-colors flex items-center justify-center gap-2"
        >
          <Icon icon="heroicons:arrow-path" class="text-xl" />
          Сбросить
        </button>
        <button
          @click="handleSave"
          :disabled="isSaving"
          class="flex-1 bg-neon text-black py-4 rounded-xl font-semibold hover:brightness-110 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <Icon v-if="!isSaving" icon="heroicons:check" class="text-xl" />
          <svg v-else class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isSaving ? 'Сохранение...' : 'Сохранить' }}</span>
        </button>
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
.accent-neon {
  accent-color: var(--color-neon);
}
</style>
