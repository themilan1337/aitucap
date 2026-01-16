<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// App version and info
const appVersion = '1.0.0'
const buildDate = 'Январь 2026'

// Features list
const features = [
  {
    icon: 'heroicons:camera',
    title: 'AI тренер',
    description: 'Искусственный интеллект отслеживает вашу технику в реальном времени через камеру'
  },
  {
    icon: 'heroicons:chart-bar',
    title: 'Персональные планы',
    description: 'Индивидуальные программы тренировок на основе ваших целей и уровня подготовки'
  },
  {
    icon: 'heroicons:fire',
    title: 'Точный подсчет',
    description: 'Автоматический подсчет повторений и калорий с высокой точностью'
  },
  {
    icon: 'heroicons:trophy',
    title: 'Достижения',
    description: 'Система мотивации с наградами за прогресс и постоянство'
  },
  {
    icon: 'heroicons:chart-pie',
    title: 'Детальная статистика',
    description: 'Отслеживайте прогресс с подробными графиками и аналитикой'
  },
  {
    icon: 'heroicons:shield-check',
    title: 'Безопасность',
    description: 'Все данные защищены, видео обрабатывается локально на устройстве'
  }
]

// Team info
const team = [
  {
    name: 'Команда AITU',
    role: 'Разработка и дизайн',
    description: 'Студенты Astana IT University'
  }
]

// Technologies
const technologies = [
  { name: 'Vue 3', icon: 'logos:vue' },
  { name: 'Nuxt 3', icon: 'logos:nuxt-icon' },
  { name: 'FastAPI', icon: 'simple-icons:fastapi' },
  { name: 'PostgreSQL', icon: 'logos:postgresql' },
  { name: 'MediaPipe', icon: 'simple-icons:google' },
  { name: 'TensorFlow', icon: 'logos:tensorflow' }
]
</script>

<template>
  <div class="px-4 pt-12 pb-24">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <button @click="router.push('/profile')" class="text-gray-400 hover:text-white">
        <Icon icon="heroicons:arrow-left" class="text-2xl" />
      </button>
      <h1 class="text-3xl font-bold">О приложении</h1>
    </div>

    <!-- App Logo & Name -->
    <div class="flex flex-col items-center mb-8">
      <div class="w-24 h-24 bg-neon rounded-3xl flex items-center justify-center mb-4 shadow-lg shadow-neon/20">
        <Icon icon="heroicons:fire" class="text-5xl text-black" />
      </div>
      <h2 class="text-2xl font-bold mb-1">AITU Cup Fitness</h2>
      <p class="text-gray-400 text-sm mb-2">Версия {{ appVersion }}</p>
      <p class="text-gray-500 text-xs">{{ buildDate }}</p>
    </div>

    <!-- Description -->
    <div class="bg-[#1A1A1A] rounded-2xl p-4 mb-6">
      <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
        <Icon icon="heroicons:information-circle" class="text-neon" />
        О проекте
      </h3>
      <p class="text-gray-300 text-sm leading-relaxed mb-3">
        AITU Cup Fitness - это инновационное приложение для фитнеса, которое использует искусственный интеллект и компьютерное зрение для отслеживания ваших тренировок в реальном времени.
      </p>
      <p class="text-gray-300 text-sm leading-relaxed">
        Наша цель - сделать фитнес доступным для каждого, предоставляя персонального AI-тренера, который помогает выполнять упражнения правильно и эффективно, где бы вы ни находились.
      </p>
    </div>

    <!-- Features Grid -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <Icon icon="heroicons:sparkles" class="text-neon" />
        Возможности
      </h3>
      <div class="grid grid-cols-1 gap-3">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="bg-[#1A1A1A] rounded-2xl p-4 hover:bg-[#222] transition-colors"
        >
          <div class="flex items-start gap-3">
            <div class="w-10 h-10 bg-neon/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <Icon :icon="feature.icon" class="text-neon text-xl" />
            </div>
            <div>
              <h4 class="font-semibold mb-1">{{ feature.title }}</h4>
              <p class="text-sm text-gray-400">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Technologies -->
    <div class="bg-[#1A1A1A] rounded-2xl p-4 mb-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <Icon icon="heroicons:code-bracket" class="text-neon" />
        Технологии
      </h3>
      <div class="grid grid-cols-3 gap-4">
        <div
          v-for="(tech, index) in technologies"
          :key="index"
          class="flex flex-col items-center gap-2 p-3 bg-[#111] rounded-xl"
        >
          <Icon :icon="tech.icon" class="text-3xl" />
          <span class="text-xs text-gray-400 text-center">{{ tech.name }}</span>
        </div>
      </div>
    </div>

    <!-- Team -->
    <div class="bg-[#1A1A1A] rounded-2xl p-4 mb-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <Icon icon="heroicons:users" class="text-neon" />
        Команда
      </h3>
      <div class="space-y-3">
        <div
          v-for="(member, index) in team"
          :key="index"
          class="flex items-center gap-4 p-3 bg-[#111] rounded-xl"
        >
          <div class="w-12 h-12 bg-neon/20 rounded-full flex items-center justify-center">
            <Icon icon="heroicons:academic-cap" class="text-neon text-2xl" />
          </div>
          <div>
            <h4 class="font-semibold">{{ member.name }}</h4>
            <p class="text-sm text-gray-400">{{ member.role }}</p>
            <p class="text-xs text-gray-500">{{ member.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Mission & Vision -->
    <div class="bg-gradient-to-br from-neon/10 to-neon/5 border border-neon/20 rounded-2xl p-4 mb-6">
      <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
        <Icon icon="heroicons:heart" class="text-neon" />
        Наша миссия
      </h3>
      <p class="text-gray-300 text-sm leading-relaxed mb-4">
        Мы верим, что каждый заслуживает доступа к качественным фитнес-тренировкам. Наша миссия - использовать передовые технологии искусственного интеллекта для создания персонализированного опыта тренировок, который мотивирует и помогает достигать целей.
      </p>
      <p class="text-gray-300 text-sm leading-relaxed">
        Мы стремимся сделать фитнес интересным, доступным и эффективным для людей любого уровня подготовки.
      </p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="bg-[#1A1A1A] rounded-2xl p-4 text-center">
        <div class="text-3xl font-bold text-neon mb-1">12+</div>
        <div class="text-xs text-gray-400">Упражнений</div>
      </div>
      <div class="bg-[#1A1A1A] rounded-2xl p-4 text-center">
        <div class="text-3xl font-bold text-neon mb-1">AI</div>
        <div class="text-xs text-gray-400">Технология</div>
      </div>
      <div class="bg-[#1A1A1A] rounded-2xl p-4 text-center">
        <div class="text-3xl font-bold text-neon mb-1">24/7</div>
        <div class="text-xs text-gray-400">Доступность</div>
      </div>
    </div>

    <!-- Contact & Social -->
    <div class="bg-[#1A1A1A] rounded-2xl p-4 mb-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <Icon icon="heroicons:chat-bubble-left-right" class="text-neon" />
        Свяжитесь с нами
      </h3>
      <div class="space-y-3">
        <a href="mailto:support@aitucup.com" class="flex items-center gap-3 p-3 bg-[#111] rounded-xl hover:bg-[#181818] transition-colors">
          <Icon icon="heroicons:envelope" class="text-neon text-xl" />
          <div>
            <div class="font-medium text-sm">Email</div>
            <div class="text-xs text-gray-400">support@aitucup.com</div>
          </div>
        </a>
        <a href="https://t.me/aitucup" target="_blank" class="flex items-center gap-3 p-3 bg-[#111] rounded-xl hover:bg-[#181818] transition-colors">
          <Icon icon="simple-icons:telegram" class="text-neon text-xl" />
          <div>
            <div class="font-medium text-sm">Telegram</div>
            <div class="text-xs text-gray-400">@aitucup</div>
          </div>
        </a>
        <a href="https://instagram.com/aitucup" target="_blank" class="flex items-center gap-3 p-3 bg-[#111] rounded-xl hover:bg-[#181818] transition-colors">
          <Icon icon="simple-icons:instagram" class="text-neon text-xl" />
          <div>
            <div class="font-medium text-sm">Instagram</div>
            <div class="text-xs text-gray-400">@aitucup</div>
          </div>
        </a>
      </div>
    </div>

    <!-- Legal Links -->
    <div class="space-y-2 mb-6">
      <button class="w-full bg-[#1A1A1A] rounded-xl p-4 text-left hover:bg-[#222] transition-colors flex items-center justify-between">
        <span class="text-sm text-gray-400">Политика конфиденциальности</span>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>
      <button class="w-full bg-[#1A1A1A] rounded-xl p-4 text-left hover:bg-[#222] transition-colors flex items-center justify-between">
        <span class="text-sm text-gray-400">Условия использования</span>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>
      <button class="w-full bg-[#1A1A1A] rounded-xl p-4 text-left hover:bg-[#222] transition-colors flex items-center justify-between">
        <span class="text-sm text-gray-400">Лицензии открытого ПО</span>
        <Icon icon="heroicons:chevron-right" class="text-gray-500" />
      </button>
    </div>

    <!-- Copyright -->
    <div class="text-center text-sm text-gray-500">
      <p>© 2026 AITU Cup Fitness</p>
      <p class="text-xs mt-1">Made with ❤️ in Kazakhstan</p>
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
