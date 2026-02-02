<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()

// App version and info
const appVersion = '1.0.0'
const buildDate = 'Февраль 2026'

// Active tab for sections
const activeTab = ref<'about' | 'tech' | 'privacy' | 'safety'>('about')

// Features list
const features = [
  {
    icon: 'heroicons:camera',
    title: 'AI Pose Detection',
    description: 'MediaPipe Pose определяет 17 ключевых точек тела с точностью 95%+'
  },
  {
    icon: 'heroicons:chart-bar',
    title: 'AI План тренировок',
    description: 'GPT-4 генерирует персонализированные 30-дневные программы'
  },
  {
    icon: 'heroicons:fire',
    title: 'Real-time анализ',
    description: 'Latency менее 50ms на кадр, 15-30 FPS обработка'
  },
  {
    icon: 'heroicons:trophy',
    title: 'Form Correction',
    description: 'Алгоритм анализа углов суставов для коррекции техники'
  },
  {
    icon: 'heroicons:chart-pie',
    title: 'Подсчет повторений',
    description: 'Автоматический подсчет через state machine с фильтрацией шума'
  },
  {
    icon: 'heroicons:shield-check',
    title: 'On-Device Processing',
    description: 'Видео обрабатывается локально, не отправляется на серверы'
  }
]

// Technologies with details
const techCategories = [
  {
    name: 'Computer Vision',
    items: [
      {
        name: 'MediaPipe Pose',
        description: 'Google ML framework',
        detail: 'Модель Full с 33 landmarks, конвертируем в COCO 17-keypoint format'
      },
      {
        name: 'COCO Keypoints',
        description: '17 точек тела',
        detail: 'Стандартный формат: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles'
      },
      {
        name: 'Angle Calculation',
        description: 'Триангуляция',
        detail: 'Вычисление углов между тремя точками для определения фазы упражнения'
      }
    ]
  },
  {
    name: 'AI & Backend',
    items: [
      {
        name: 'Azure OpenAI GPT-4',
        description: 'План генерация',
        detail: 'Structured output с Pydantic schemas для 30-дневных программ'
      },
      {
        name: 'FastAPI',
        description: 'Async Python',
        detail: 'WebSocket для real-time, JWT auth, rate limiting'
      },
      {
        name: 'PostgreSQL + Redis',
        description: 'Data layer',
        detail: 'Async SQLAlchemy ORM, Redis для сессий и CSRF токенов'
      }
    ]
  },
  {
    name: 'Frontend',
    items: [
      {
        name: 'Nuxt 4 + Vue 3',
        description: 'Web framework',
        detail: 'Composition API, Pinia state management, TypeScript'
      },
      {
        name: 'TailwindCSS',
        description: 'Styling',
        detail: 'Utility-first CSS с кастомными neon цветами'
      },
      {
        name: 'Chart.js',
        description: 'Визуализация',
        detail: 'Графики прогресса и статистики тренировок'
      }
    ]
  }
]

// Performance metrics
const metrics = [
  { label: 'Pose Detection', value: '<50ms', description: 'latency per frame' },
  { label: 'Keypoint Accuracy', value: '95%+', description: 'detection rate' },
  { label: 'Processing FPS', value: '15-30', description: 'frames per second' },
  { label: 'Supported Exercises', value: '12', description: 'exercise types' },
]

// Privacy points
const privacyPoints = [
  {
    icon: 'heroicons:video-camera-slash',
    title: 'Никаких записей видео',
    description: 'Видеопоток обрабатывается в реальном времени и не сохраняется ни локально, ни на серверах. После закрытия камеры данные удаляются.'
  },
  {
    icon: 'heroicons:cpu-chip',
    title: 'On-Device Processing',
    description: 'Pose detection выполняется полностью на вашем устройстве через MediaPipe в браузере. Никакие кадры не отправляются на внешние серверы.'
  },
  {
    icon: 'heroicons:lock-closed',
    title: 'Шифрование данных',
    description: 'Все API запросы передаются по HTTPS с TLS 1.3. Токены аутентификации хранятся в HttpOnly Secure cookies.'
  },
  {
    icon: 'heroicons:finger-print',
    title: 'Минимум данных',
    description: 'Мы собираем только необходимые данные: email для аутентификации, параметры профиля для персонализации, статистику тренировок для отслеживания прогресса.'
  },
  {
    icon: 'heroicons:trash',
    title: 'Право на удаление',
    description: 'Вы можете запросить полное удаление вашего аккаунта и всех связанных данных в любое время через настройки профиля.'
  },
  {
    icon: 'heroicons:globe-alt',
    title: 'GDPR Compliance',
    description: 'Мы следуем принципам GDPR в части обработки персональных данных, включая прозрачность, минимизацию данных и право на доступ.'
  }
]

// Safety warnings
const safetyPoints = [
  {
    icon: 'heroicons:heart',
    title: 'Консультация с врачом',
    description: 'Перед началом любой программы тренировок рекомендуется проконсультироваться с врачом, особенно при наличии хронических заболеваний, травм или беременности.'
  },
  {
    icon: 'heroicons:exclamation-triangle',
    title: 'Не замена специалиста',
    description: 'MuscleUp Vision является инструментом для самостоятельных тренировок и не заменяет профессионального тренера или физиотерапевта.'
  },
  {
    icon: 'heroicons:hand-raised',
    title: 'Прекратите при боли',
    description: 'Немедленно прекратите упражнение, если чувствуете острую боль, головокружение или дискомфорт. Прислушивайтесь к своему телу.'
  },
  {
    icon: 'heroicons:arrow-path',
    title: 'Разминка обязательна',
    description: 'Всегда выполняйте разминку перед тренировкой и заминку после. Это снижает риск травм и улучшает восстановление.'
  },
  {
    icon: 'heroicons:beaker',
    title: 'Индивидуальные особенности',
    description: 'Алгоритм может не учитывать ваши индивидуальные анатомические особенности. При сомнениях консультируйтесь со специалистом.'
  },
  {
    icon: 'heroicons:shield-exclamation',
    title: 'Ответственность',
    description: 'Пользователь принимает на себя полную ответственность за своё здоровье при использовании приложения. Разработчики не несут ответственности за травмы.'
  }
]

// Team
const team = [
  {
    name: 'Sultan Karilov',
    role: 'AI Engineer',
    avatar: 'https://media.licdn.com/dms/image/v2/D4D03AQHMj_uHKPgGuw/profile-displayphoto-scale_400_400/B4DZfBaOWhHkAg-/0/1751296568413?e=1770249600&v=beta&t=zISIJQYVypXwG8_6SaFHVpyo9coQlboH-BIAsw4oLXI'
  },
  {
    name: 'Bizhan Ashyhatov',
    role: 'iOS & AI Engineer',
    avatar: 'https://media.licdn.com/dms/image/v2/D4D03AQGsONoaf48xcw/profile-displayphoto-shrink_400_400/B4DZhhQaPSHwAg-/0/1753978350464?e=1770249600&v=beta&t=YBY6_0-WJchv9twLQbncybJBeTT74-Z4cODUO3MUPqs'
  },
  {
    name: 'Milan Gorislavets',
    role: 'Fullstack Engineer',
    avatar: 'https://media.licdn.com/dms/image/v2/D4E03AQE4nmQk2sW0kA/profile-displayphoto-scale_400_400/B4EZqndwLsKcAg-/0/1763746207137?e=1770249600&v=beta&t=RPx_xsg0ZaC58j-oppLiCuT81REaVdeSfbl97KZ7wAI'
  }
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
    <div class="flex flex-col items-center mb-6">
      <div class="w-20 h-20 bg-neon rounded-3xl flex items-center justify-center mb-3 shadow-lg shadow-neon/20">
        <Icon icon="heroicons:fire" class="text-4xl text-black" />
      </div>
      <h2 class="text-xl font-bold mb-1">MuscleUp Vision</h2>
      <p class="text-gray-400 text-sm">v{{ appVersion }} • {{ buildDate }}</p>
    </div>

    <!-- Tab Navigation -->
    <div class="flex p-1 bg-[#1A1A1A] rounded-2xl mb-6 overflow-x-auto">
      <button
        v-for="tab in [
          { id: 'about', label: 'О проекте', icon: 'heroicons:information-circle' },
          { id: 'tech', label: 'Технологии', icon: 'heroicons:cpu-chip' },
          { id: 'privacy', label: 'Privacy', icon: 'heroicons:lock-closed' },
          { id: 'safety', label: 'Safety', icon: 'heroicons:shield-check' }
        ]"
        :key="tab.id"
        @click="activeTab = tab.id as any"
        class="flex-1 min-w-[80px] py-2 px-3 text-xs font-medium rounded-xl transition-all duration-200 flex items-center justify-center gap-1"
        :class="activeTab === tab.id ? 'bg-neon text-black' : 'text-gray-400 hover:text-white'"
      >
        <Icon :icon="tab.icon" class="text-sm" />
        {{ tab.label }}
      </button>
    </div>

    <!-- About Tab -->
    <div v-if="activeTab === 'about'">
      <!-- Description -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4 mb-6">
        <p class="text-gray-300 text-sm leading-relaxed mb-3">
          MuscleUp Vision — AI-powered fitness приложение, использующее компьютерное зрение для анализа техники упражнений в реальном времени.
        </p>
        <p class="text-gray-400 text-sm leading-relaxed">
          Наша цель — сделать качественные фитнес-тренировки доступными для каждого, предоставляя персонального AI-тренера без необходимости в дополнительном оборудовании.
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
            class="bg-[#1A1A1A] rounded-2xl p-4"
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

      <!-- Performance Metrics -->
      <div class="grid grid-cols-2 gap-3 mb-6">
        <div
          v-for="(metric, index) in metrics"
          :key="index"
          class="bg-[#1A1A1A] rounded-2xl p-4 text-center"
        >
          <div class="text-2xl font-bold text-neon mb-1">{{ metric.value }}</div>
          <div class="text-xs text-white font-medium">{{ metric.label }}</div>
          <div class="text-xs text-gray-500">{{ metric.description }}</div>
        </div>
      </div>

      <!-- Team -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4 mb-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <Icon icon="heroicons:users" class="text-neon" />
          Команда
        </h3>
        <div class="flex justify-center gap-6">
          <div
            v-for="(member, index) in team"
            :key="index"
            class="text-center"
          >
            <img
              :src="member.avatar"
              :alt="member.name"
              class="w-16 h-16 rounded-full mx-auto mb-2 border-2 border-neon/30"
            />
            <p class="text-sm font-medium">{{ member.name.split(' ')[0] }}</p>
            <p class="text-xs text-gray-500">{{ member.role }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Technology Tab -->
    <div v-if="activeTab === 'tech'">
      <div class="space-y-6">
        <div
          v-for="(category, index) in techCategories"
          :key="index"
          class="bg-[#1A1A1A] rounded-2xl p-4"
        >
          <h3 class="text-neon font-semibold mb-4">{{ category.name }}</h3>
          <div class="space-y-4">
            <div
              v-for="(item, idx) in category.items"
              :key="idx"
              class="border-l-2 border-neon/30 pl-3"
            >
              <div class="flex items-center gap-2 mb-1">
                <span class="font-medium text-sm">{{ item.name }}</span>
                <span class="text-xs text-gray-500">{{ item.description }}</span>
              </div>
              <p class="text-xs text-gray-400">{{ item.detail }}</p>
            </div>
          </div>
        </div>

        <!-- Architecture -->
        <div class="bg-[#1A1A1A] rounded-2xl p-4">
          <h3 class="font-semibold mb-4 flex items-center gap-2">
            <Icon icon="heroicons:squares-2x2" class="text-neon" />
            Архитектура
          </h3>
          <div class="flex flex-wrap items-center justify-center gap-2 text-xs">
            <span class="px-3 py-1.5 bg-neon/10 text-neon rounded-lg">Camera</span>
            <Icon icon="heroicons:arrow-right" class="text-gray-600" />
            <span class="px-3 py-1.5 bg-blue-500/10 text-blue-400 rounded-lg">MediaPipe</span>
            <Icon icon="heroicons:arrow-right" class="text-gray-600" />
            <span class="px-3 py-1.5 bg-purple-500/10 text-purple-400 rounded-lg">Angles</span>
            <Icon icon="heroicons:arrow-right" class="text-gray-600" />
            <span class="px-3 py-1.5 bg-green-500/10 text-green-400 rounded-lg">Counter</span>
            <Icon icon="heroicons:arrow-right" class="text-gray-600" />
            <span class="px-3 py-1.5 bg-orange-500/10 text-orange-400 rounded-lg">UI</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Privacy Tab -->
    <div v-if="activeTab === 'privacy'">
      <div class="bg-gradient-to-br from-blue-500/10 to-blue-500/5 border border-blue-500/20 rounded-2xl p-4 mb-6">
        <h3 class="font-semibold mb-2 flex items-center gap-2">
          <Icon icon="heroicons:shield-check" class="text-blue-400" />
          Privacy First
        </h3>
        <p class="text-sm text-gray-400">
          Мы серьёзно относимся к вашей конфиденциальности. Ваши данные — ваша собственность.
        </p>
      </div>

      <div class="space-y-3">
        <div
          v-for="(point, index) in privacyPoints"
          :key="index"
          class="bg-[#1A1A1A] rounded-2xl p-4"
        >
          <div class="flex items-start gap-3">
            <div class="w-10 h-10 bg-blue-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <Icon :icon="point.icon" class="text-blue-400 text-xl" />
            </div>
            <div>
              <h4 class="font-semibold mb-1 text-sm">{{ point.title }}</h4>
              <p class="text-xs text-gray-400">{{ point.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Data we collect -->
      <div class="bg-[#1A1A1A] rounded-2xl p-4 mt-6">
        <h3 class="font-semibold mb-3 text-sm">Какие данные мы собираем</h3>
        <ul class="space-y-2 text-xs text-gray-400">
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:check" class="text-green-500 mt-0.5" />
            <span>Email и имя (для аутентификации)</span>
          </li>
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:check" class="text-green-500 mt-0.5" />
            <span>Параметры профиля: возраст, вес, рост, цели (для персонализации)</span>
          </li>
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:check" class="text-green-500 mt-0.5" />
            <span>Статистика тренировок: повторения, калории, точность (для прогресса)</span>
          </li>
          <li class="flex items-start gap-2">
            <Icon icon="heroicons:x-mark" class="text-red-500 mt-0.5" />
            <span>НЕ собираем: видеозаписи, фотографии, геолокацию</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Safety Tab -->
    <div v-if="activeTab === 'safety'">
      <div class="bg-gradient-to-br from-orange-500/10 to-orange-500/5 border border-orange-500/20 rounded-2xl p-4 mb-6">
        <h3 class="font-semibold mb-2 flex items-center gap-2">
          <Icon icon="heroicons:exclamation-triangle" class="text-orange-400" />
          Важное предупреждение
        </h3>
        <p class="text-sm text-gray-400">
          MuscleUp Vision является инструментом для самостоятельных тренировок и не является медицинским устройством.
        </p>
      </div>

      <div class="space-y-3">
        <div
          v-for="(point, index) in safetyPoints"
          :key="index"
          class="bg-[#1A1A1A] rounded-2xl p-4"
        >
          <div class="flex items-start gap-3">
            <div class="w-10 h-10 bg-orange-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <Icon :icon="point.icon" class="text-orange-400 text-xl" />
            </div>
            <div>
              <h4 class="font-semibold mb-1 text-sm">{{ point.title }}</h4>
              <p class="text-xs text-gray-400">{{ point.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Medical Disclaimer -->
      <div class="bg-red-500/10 border border-red-500/30 rounded-2xl p-4 mt-6">
        <h3 class="font-semibold mb-2 text-sm text-red-400">Medical Disclaimer</h3>
        <p class="text-xs text-gray-400 leading-relaxed">
          Информация и функции, предоставляемые MuscleUp Vision, предназначены только для образовательных и информационных целей.
          Они не предназначены для диагностики, лечения или профилактики каких-либо заболеваний.
          Всегда консультируйтесь с квалифицированным медицинским специалистом перед началом любой программы упражнений.
          Использование приложения осуществляется на ваш собственный риск.
        </p>
      </div>
    </div>

    <!-- Contact Section (always visible) -->
    <div class="mt-6 bg-[#1A1A1A] rounded-2xl p-4">
      <h3 class="text-sm font-semibold mb-3 flex items-center gap-2">
        <Icon icon="heroicons:chat-bubble-left-right" class="text-neon" />
        Контакты
      </h3>
      <div class="flex gap-3">
        <a href="https://github.com/themilan1337/aitucup" target="_blank" class="flex-1 flex items-center justify-center gap-2 p-3 bg-[#111] rounded-xl hover:bg-[#181818] transition-colors">
          <Icon icon="simple-icons:github" class="text-xl" />
          <span class="text-xs">GitHub</span>
        </a>
        <a href="https://muscleup.fitness" target="_blank" class="flex-1 flex items-center justify-center gap-2 p-3 bg-[#111] rounded-xl hover:bg-[#181818] transition-colors">
          <Icon icon="heroicons:globe-alt" class="text-xl text-neon" />
          <span class="text-xs">Website</span>
        </a>
      </div>
    </div>

    <!-- Copyright -->
    <div class="text-center text-xs text-gray-500 mt-6">
      <p>© 2026 MuscleUp Vision • AITU CAP</p>
      <p class="mt-1">Made with 💚 in Kazakhstan</p>
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
