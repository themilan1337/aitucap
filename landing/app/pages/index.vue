<script setup lang="ts">
import { Icon } from '@iconify/vue'

const features = [
  {
    icon: 'hugeicons:ai-brain-05',
    title: 'Анализ в реальном времени',
    description: 'Компьютерное зрение отслеживает ваши движения и анализирует технику выполнения упражнений мгновенно',
  },
  {
    icon: 'hugeicons:voice',
    title: 'ИИ-тренер',
    description: 'Искусственный интеллект дает мгновенные рекомендации и корректирует технику как персональный тренер',
  },
  {
    icon: 'hugeicons:workout-run',
    title: 'Персональный план',
    description: 'Индивидуальная программа тренировок, адаптированная под ваш уровень и цели',
  },
  {
    icon: 'hugeicons:analytics-up',
    title: 'Отслеживание прогресса',
    description: 'Подробная статистика тренировок, калорий и достижений для мотивации',
  },
]

const steps = [
  {
    number: 1,
    icon: 'hugeicons:camera-01',
    title: 'Камера определяет положение тела',
    description: 'Технология компьютерного зрения распознает ключевые точки вашего тела',
  },
  {
    number: 2,
    icon: 'hugeicons:ai-brain-01',
    title: 'ИИ анализирует технику',
    description: 'Нейросеть оценивает правильность выполнения упражнения в реальном времени',
  },
  {
    number: 3,
    icon: 'hugeicons:alert-02',
    title: 'Приложение подсказывает',
    description: 'Получайте мгновенную обратную связь, если техника нарушена',
  },
]

const benefits = [
  {
    icon: 'hugeicons:shield-check',
    title: 'Безопасные тренировки',
    description: 'Предотвращайте травмы благодаря контролю техники',
  },
  {
    icon: 'hugeicons:trophy',
    title: 'Эффективные результаты',
    description: 'Правильная техника = максимальный результат',
  },
  {
    icon: 'hugeicons:user-account',
    title: 'Персональный тренер',
    description: 'Тренируйтесь как с профессиональным тренером',
  },
  {
    icon: 'hugeicons:chart-increase',
    title: 'Видимый прогресс',
    description: 'Отслеживайте улучшения каждый день',
  },
]

const techStack = [
  {
    category: 'Computer Vision',
    items: [
      { name: 'MediaPipe Pose', description: 'Google\'s ML framework for pose detection' },
      { name: 'RTMPose', description: 'Real-Time Multi-Person Pose Estimation' },
      { name: 'COCO 17-Keypoint', description: 'Industry-standard body keypoint format' },
    ]
  },
  {
    category: 'AI & Backend',
    items: [
      { name: 'Azure OpenAI GPT-4', description: 'Intelligent workout plan generation' },
      { name: 'FastAPI', description: 'High-performance async Python backend' },
      { name: 'WebSocket', description: 'Real-time bidirectional communication' },
    ]
  },
  {
    category: 'Frontend & Mobile',
    items: [
      { name: 'Nuxt.js 4 + Vue 3', description: 'Modern reactive web framework' },
      { name: 'Swift + SwiftUI', description: 'Native iOS development' },
      { name: 'TailwindCSS', description: 'Utility-first CSS framework' },
    ]
  }
]

const performanceMetrics = [
  { label: 'Latency', value: '<50ms', description: 'Per frame processing' },
  { label: 'Accuracy', value: '95%+', description: 'Keypoint detection' },
  { label: 'FPS', value: '15-30', description: 'Frames per second' },
  { label: 'Exercises', value: '12+', description: 'Supported exercises' },
]

const safetyFeatures = [
  {
    icon: 'hugeicons:shield-check',
    title: 'On-Device Processing',
    description: 'Видео обрабатывается локально на вашем устройстве. Никакие видеозаписи не отправляются на серверы.'
  },
  {
    icon: 'hugeicons:lock-key',
    title: 'Шифрование данных',
    description: 'Все данные передаются по защищенному HTTPS соединению с TLS 1.3 шифрованием.'
  },
  {
    icon: 'hugeicons:user-shield-02',
    title: 'GDPR Compliant',
    description: 'Мы соблюдаем европейские стандарты защиты персональных данных.'
  },
  {
    icon: 'hugeicons:stethoscope',
    title: 'Медицинский дисклеймер',
    description: 'Приложение не заменяет консультацию врача. Перед началом тренировок проконсультируйтесь со специалистом.'
  }
]

const roadmapItems = [
  {
    quarter: 'Q1 2026',
    status: 'current',
    title: 'MVP Launch',
    items: ['iOS приложение', 'Веб-платформа', '12 базовых упражнений', 'AI планы тренировок']
  },
  {
    quarter: 'Q2 2026',
    status: 'upcoming',
    title: 'Expansion',
    items: ['Android приложение', 'Apple Watch интеграция', '30+ упражнений', 'Голосовой AI-тренер']
  },
  {
    quarter: 'Q3 2026',
    status: 'planned',
    title: 'B2B Launch',
    items: ['Corporate Wellness', 'API для партнёров', 'Групповые тренировки', 'Аналитика для HR']
  },
  {
    quarter: 'Q4 2026',
    status: 'planned',
    title: 'Global Scale',
    items: ['Международный запуск', 'Мультиязычность', 'AI персонализация 2.0', 'Интеграция с фитнес-трекерами']
  }
]

const competitors = [
  { name: 'MuscleUp Vision', realTimePose: true, noHardware: true, aiPlans: true, formCorrection: true, free: true },
  { name: 'Fitbit Premium', realTimePose: false, noHardware: false, aiPlans: false, formCorrection: false, free: false },
  { name: 'Nike Training', realTimePose: false, noHardware: true, aiPlans: false, formCorrection: false, free: true },
  { name: 'Peloton', realTimePose: false, noHardware: false, aiPlans: false, formCorrection: true, free: false },
  { name: 'Apple Fitness+', realTimePose: false, noHardware: false, aiPlans: false, formCorrection: false, free: false },
]

const faqItems = [
  {
    question: 'Какие упражнения поддерживаются?',
    answer: 'В текущей версии поддерживается 12 упражнений: приседания, отжимания, выпады, планка, скручивания, подъемы корпуса, сгибания на бицепс, боковые подъемы, жим над головой, подъемы ног, подъемы коленей и жим коленями. Мы постоянно добавляем новые упражнения.'
  },
  {
    question: 'Нужен ли интернет для тренировок?',
    answer: 'Для анализа движений интернет не требуется — pose detection работает полностью локально на устройстве. Интернет нужен только для синхронизации статистики и генерации AI планов.'
  },
  {
    question: 'Какие устройства поддерживаются?',
    answer: 'Веб-версия работает в любом современном браузере (Chrome, Safari, Firefox). iOS приложение доступно для iPhone с iOS 15+. Android версия находится в разработке.'
  },
  {
    question: 'Приложение бесплатное?',
    answer: 'Да, базовая версия полностью бесплатна. В будущем мы планируем добавить Premium подписку с расширенными функциями, но core функциональность останется бесплатной.'
  },
  {
    question: 'Насколько точно определяется техника?',
    answer: 'Наша система использует MediaPipe Pose от Google с точностью определения ключевых точек тела 95%+. Алгоритм анализа техники обучен на тысячах примеров правильного выполнения упражнений.'
  }
]

const team = [
  {
    name: 'Sultan Karilov',
    role: 'AI Engineer',
    avatar: '/sultan.png',
    education: 'MBZUAI, Class Of 2030',
    experience: 'AI Engineer @ Zimran, основал Runvex (1000+ пользователей), выпускник nFactorial Incubator',
    responsibilities: [
      'Определяет стратегию развития продукта',
      'Отвечает за ИИ-модели и персонализацию тренировок',
      'Финансы и управление компанией',
      'Контроль ресурсов и планирование развития'
    ],
    social: {
      linkedin: 'https://www.linkedin.com/in/sultan-karilov-a9abb1362/',
      github: 'https://github.com/sulta24'
    }
  },
  {
    name: 'Bizhan Ashyhatov',
    role: 'iOS & AI Engineer',
    avatar: '/bizhan.jpeg',
    education: 'AITU, 2 курс',
    experience: 'Основатель AuarAI (приобретена), CO-CEO в BachOpus, приложения с аудиторией 50k+, выпускник nFactorial Incubator',
    responsibilities: [
      'Разработка iOS-приложения',
      'Интеграция ИИ-моделей',
      'Обеспечение стабильной работы на мобильных устройствах',
      'Маркетинг и управление продвижением продукта'
    ],
    social: {
      linkedin: 'https://www.linkedin.com/in/bizhanchik/',
      github: 'https://github.com/bizhanchik/'
    }
  },
  {
    name: 'Milan Gorislavets',
    role: 'Fullstack Engineer',
    avatar: '/milan.jpeg',
    education: 'Seitzhan School',
    experience: 'Основатель SereneAI, CatOps, fckvibecode, ведущий frontend инженер',
    responsibilities: [
      'Разработка фронтенда и бэкенда',
      'Интеграция базы данных и облачных сервисов',
      'Дизайн и креативные материалы',
      'UI/UX, визуальная коммуникация и контент для продвижения'
    ],
    social: {
      linkedin: 'https://linkedin.com/in/milangorislavetz',
      github: 'https://github.com/milan'
    }
  }
]
</script>

<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section relative min-h-screen flex items-center justify-center overflow-hidden">
      <!-- Background Effects -->
      <div class="absolute inset-0 bg-gradient-radial from-neon/5 via-transparent to-transparent opacity-50"></div>
      <div class="absolute top-20 left-1/4 w-96 h-96 bg-neon/10 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-neon/5 rounded-full blur-[100px]"></div>

      <div class="container mx-auto px-6 py-20 relative z-10">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Text Content -->
          <div class="hero-content space-y-8">
            <div class="space-y-4">
              <div class="inline-block px-4 py-2 bg-neon/10 border border-neon/30 rounded-full text-neon text-sm font-medium backdrop-blur-sm">
                AITU CAP 2026
              </div>
              <h1 class="text-5xl md:text-7xl font-bold leading-tight">
                Тренируйтесь <br />
                <span class="text-neon glow-text">правильно</span> с <br />
                помощью ИИ
              </h1>
            </div>

            <p class="text-xl text-gray-400 max-w-xl">
              MuscleUp Vision использует компьютерное зрение для анализа техники упражнений.
              Тренируйтесь безопасно и эффективно с персональным ИИ-тренером.
            </p>

            <div class="flex flex-col sm:flex-row gap-4">
              <NuxtLink to="https://app.muscleup.fitness/"
                class="group px-8 py-4 bg-neon text-black font-bold text-lg rounded-2xl hover:brightness-110 transition-all duration-300 shadow-neon hover:shadow-neon-lg flex items-center justify-center gap-3"
              >
                Начать тренировку
                <Icon icon="hugeicons:arrow-right-02" class="text-2xl group-hover:translate-x-1 transition-transform" />
              </NuxtLink>
              <a
                href="#demo"
                class="px-8 py-4 bg-white/5 border border-white/10 text-white font-bold text-lg rounded-2xl hover:bg-white/10 hover:border-neon/50 transition-all duration-300 backdrop-blur-sm flex items-center justify-center gap-3"
              >
                <Icon icon="hugeicons:play" class="text-xl" />
                Смотреть демо
              </a>
            </div>

            <!-- Stats -->
            <div class="flex gap-8 pt-8">
              <div>
                <div class="text-3xl font-bold text-neon">95%</div>
                <div class="text-sm text-gray-500">Точность анализа</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-neon">24/7</div>
                <div class="text-sm text-gray-500">Доступность</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-neon">0₸</div>
                <div class="text-sm text-gray-500">Бесплатно</div>
              </div>
            </div>
          </div>

          <!-- Hero Image -->
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-t from-neon/20 via-transparent to-transparent rounded-3xl blur-2xl"></div>
            <div class="relative">
              <img
                src="/girl.png"
                alt="MuscleUp Vision AI Fitness"
                class="w-full h-auto drop-shadow-2xl"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-32 relative">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Возможности <span class="text-neon">платформы</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Передовые технологии искусственного интеллекта для вашего прогресса
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="feature-card group bg-card rounded-3xl p-8 hover:bg-card-hover transition-all duration-300 border border-white/5 hover:border-neon/50 hover:shadow-neon-card"
          >
            <div class="w-16 h-16 rounded-2xl bg-neon/10 flex items-center justify-center mb-6 group-hover:bg-neon/20 transition-all duration-300">
              <Icon :icon="feature.icon" class="text-4xl text-neon" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ feature.title }}</h3>
            <p class="text-gray-400 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works-section py-32 relative">
      <!-- Background Effect -->
      <div class="absolute inset-0 bg-gradient-to-b from-transparent via-neon/5 to-transparent"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="text-center mb-20 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Как это <span class="text-neon">работает</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Три простых шага до идеальной техники выполнения упражнений
          </p>
        </div>

        <div class="max-w-5xl mx-auto space-y-8">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="step-card relative"
          >
            <div class="flex flex-col md:flex-row gap-8 items-start md:items-center bg-card rounded-3xl p-8 border border-white/5 hover:border-neon/30 transition-all duration-300 hover:shadow-neon-card">
              <div class="flex-shrink-0 relative">
                <div class="w-32 h-32 rounded-2xl bg-neon flex items-center justify-center shadow-neon">
                  <Icon :icon="step.icon" class="text-6xl text-black" />
                </div>
                <div class="absolute -top-3 -right-3 w-12 h-12 rounded-xl bg-black border-2 border-neon flex items-center justify-center text-2xl font-bold text-neon">
                  {{ step.number }}
                </div>
              </div>

              <!-- Step Content -->
              <div class="flex-1 space-y-3">
                <h3 class="text-2xl font-bold">{{ step.title }}</h3>
                <p class="text-lg text-gray-400 leading-relaxed">{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits Section -->
    <section class="benefits-section py-32 relative">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Почему <span class="text-neon">MuscleUp Vision</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Преимущества тренировок с искусственным интеллектом
          </p>
        </div>

        <div class="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <div
            v-for="(benefit, index) in benefits"
            :key="index"
            class="benefit-card group bg-gradient-to-br from-card to-card-hover rounded-3xl p-10 border border-white/5 hover:border-neon/50 transition-all duration-300 hover:shadow-neon-card"
          >
            <div class="flex items-start gap-6">
              <div class="w-20 h-20 rounded-2xl bg-neon/10 flex items-center justify-center flex-shrink-0 group-hover:bg-neon/20 transition-all duration-300">
                <Icon :icon="benefit.icon" class="text-5xl text-neon" />
              </div>
              <div class="space-y-3">
                <h3 class="text-2xl font-bold">{{ benefit.title }}</h3>
                <p class="text-gray-400 text-lg leading-relaxed">{{ benefit.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Live Demo Section -->
    <section id="demo" class="demo-section py-32 relative">
      <div class="absolute inset-0 bg-gradient-to-b from-transparent via-neon/5 to-transparent"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="text-center mb-16 space-y-4">
          <div class="inline-block px-4 py-2 bg-neon/10 border border-neon/30 rounded-full text-neon text-sm font-medium mb-4">
            СМОТРИТЕ В ДЕЙСТВИИ
          </div>
          <h2 class="text-4xl md:text-6xl font-bold">
            <span class="text-neon">AI</span> в действии
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Посмотрите, как компьютерное зрение анализирует технику выполнения упражнений в реальном времени
          </p>
        </div>

        <!-- Video Demo -->
        <div class="max-w-4xl mx-auto">
          <div class="relative rounded-3xl overflow-hidden bg-[#111] border border-white/10 aspect-video group hover:border-neon/50 transition-all duration-300">
            <video
              class="absolute inset-0 w-full h-full object-cover"
              autoplay
              loop
              muted
              playsinline
              preload="auto"
              poster="/screenshots/training.png"
            >
              <source src="/demo-video.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>

          <!-- Demo Features -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
            <div class="bg-[#111] rounded-2xl p-4 text-center border border-white/5">
              <Icon icon="hugeicons:body-part-muscle" class="text-3xl text-neon mx-auto mb-2" />
              <p class="text-sm text-gray-400">17 точек тела</p>
            </div>
            <div class="bg-[#111] rounded-2xl p-4 text-center border border-white/5">
              <Icon icon="hugeicons:time-quarter-pass" class="text-3xl text-neon mx-auto mb-2" />
              <p class="text-sm text-gray-400">&lt;50ms latency</p>
            </div>
            <div class="bg-[#111] rounded-2xl p-4 text-center border border-white/5">
              <Icon icon="hugeicons:chart-line-data-01" class="text-3xl text-neon mx-auto mb-2" />
              <p class="text-sm text-gray-400">Real-time анализ</p>
            </div>
            <div class="bg-[#111] rounded-2xl p-4 text-center border border-white/5">
              <Icon icon="hugeicons:checkmark-circle-02" class="text-3xl text-neon mx-auto mb-2" />
              <p class="text-sm text-gray-400">95%+ точность</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- App Screenshots Section -->
    <section class="screenshots-section py-32 relative overflow-hidden">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Приложение <span class="text-neon">MuscleUp</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Интуитивный интерфейс для эффективных тренировок
          </p>
        </div>

        <!-- Phone Mockups -->
        <div class="flex justify-center items-center gap-4 md:gap-8 overflow-x-auto pb-8">
          <!-- Screen 1: Training -->
          <div class="flex-shrink-0 relative">
            <div class="w-[200px] md:w-[280px] h-[400px] md:h-[560px] bg-[#111] rounded-[40px] p-2 border-4 border-gray-800 shadow-2xl">
              <div class="w-full h-full bg-black rounded-[32px] overflow-hidden relative">
                <img src="/screenshots/training.png" alt="Training Screen" class="w-full h-full object-cover" />
              </div>
              <!-- Notch -->
              <div class="absolute top-4 left-1/2 -translate-x-1/2 w-20 h-6 bg-black rounded-full"></div>
            </div>
            <p class="text-center text-sm text-gray-400 mt-4">Тренировка</p>
          </div>

          <!-- Screen 2: Home (Featured) -->
          <div class="flex-shrink-0 relative transform scale-105 md:scale-110 z-10">
            <div class="w-[220px] md:w-[300px] h-[440px] md:h-[600px] bg-[#111] rounded-[44px] p-2 border-4 border-neon/50 shadow-[0_0_40px_rgba(204,255,0,0.2)]">
              <div class="w-full h-full bg-black rounded-[36px] overflow-hidden relative">
                <img src="/screenshots/home.png" alt="Home Screen" class="w-full h-full object-cover" />
              </div>
              <div class="absolute top-4 left-1/2 -translate-x-1/2 w-24 h-7 bg-black rounded-full"></div>
            </div>
            <p class="text-center text-sm text-neon font-medium mt-4">Главная</p>
          </div>

          <!-- Screen 3: Progress -->
          <div class="flex-shrink-0 relative">
            <div class="w-[200px] md:w-[280px] h-[400px] md:h-[560px] bg-[#111] rounded-[40px] p-2 border-4 border-gray-800 shadow-2xl">
              <div class="w-full h-full bg-black rounded-[32px] overflow-hidden relative">
                <img src="/screenshots/progress.png" alt="Progress Screen" class="w-full h-full object-cover" />
              </div>
              <div class="absolute top-4 left-1/2 -translate-x-1/2 w-20 h-6 bg-black rounded-full"></div>
            </div>
            <p class="text-center text-sm text-gray-400 mt-4">Прогресс</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Technology Stack Section -->
    <section id="technology" class="tech-section py-32 relative">
      <div class="absolute inset-0 bg-gradient-to-b from-neon/5 via-transparent to-neon/5"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="text-center mb-16 space-y-4">
          <div class="inline-block px-4 py-2 bg-neon/10 border border-neon/30 rounded-full text-neon text-sm font-medium mb-4">
            TECH STACK
          </div>
          <h2 class="text-4xl md:text-6xl font-bold">
            Технологии <span class="text-neon">под капотом</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Современный стек технологий для максимальной производительности
          </p>
        </div>

        <!-- Tech Categories -->
        <div class="grid md:grid-cols-3 gap-8 mb-16">
          <div
            v-for="(category, index) in techStack"
            :key="index"
            class="bg-[#111] rounded-3xl p-8 border border-white/5 hover:border-neon/30 transition-all duration-300"
          >
            <h3 class="text-xl font-bold text-neon mb-6">{{ category.category }}</h3>
            <div class="space-y-4">
              <div
                v-for="(item, idx) in category.items"
                :key="idx"
                class="flex items-start gap-3"
              >
                <Icon icon="hugeicons:checkmark-circle-02" class="text-neon text-lg mt-1 flex-shrink-0" />
                <div>
                  <p class="font-medium text-white">{{ item.name }}</p>
                  <p class="text-sm text-gray-500">{{ item.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="bg-[#111] rounded-3xl p-8 border border-white/5">
          <h3 class="text-2xl font-bold text-center mb-8">Производительность</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div
              v-for="(metric, index) in performanceMetrics"
              :key="index"
              class="text-center"
            >
              <p class="text-4xl md:text-5xl font-bold text-neon mb-2">{{ metric.value }}</p>
              <p class="text-white font-medium">{{ metric.label }}</p>
              <p class="text-sm text-gray-500">{{ metric.description }}</p>
            </div>
          </div>
        </div>

        <!-- Architecture Diagram Placeholder -->
        <div class="mt-12 bg-[#0a0a0a] rounded-3xl p-8 border border-white/5">
          <h3 class="text-xl font-bold text-center mb-6">Архитектура системы</h3>
          <div class="flex flex-wrap justify-center items-center gap-4 text-sm">
            <div class="px-4 py-2 bg-neon/10 text-neon rounded-lg">📱 Camera</div>
            <Icon icon="hugeicons:arrow-right-02" class="text-gray-600" />
            <div class="px-4 py-2 bg-blue-500/10 text-blue-400 rounded-lg">🧠 MediaPipe Pose</div>
            <Icon icon="hugeicons:arrow-right-02" class="text-gray-600" />
            <div class="px-4 py-2 bg-purple-500/10 text-purple-400 rounded-lg">📐 Angle Calculator</div>
            <Icon icon="hugeicons:arrow-right-02" class="text-gray-600" />
            <div class="px-4 py-2 bg-green-500/10 text-green-400 rounded-lg">🔢 Rep Counter</div>
            <Icon icon="hugeicons:arrow-right-02" class="text-gray-600" />
            <div class="px-4 py-2 bg-orange-500/10 text-orange-400 rounded-lg">✨ UI Feedback</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Safety & Privacy Section -->
    <section id="privacy" class="safety-section py-32 relative">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Безопасность и <span class="text-neon">приватность</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Ваши данные под надёжной защитой
          </p>
        </div>

        <div class="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          <div
            v-for="(feature, index) in safetyFeatures"
            :key="index"
            class="bg-[#111] rounded-3xl p-8 border border-white/5 hover:border-neon/30 transition-all duration-300"
          >
            <div class="flex items-start gap-6">
              <div class="w-16 h-16 rounded-2xl bg-neon/10 flex items-center justify-center flex-shrink-0">
                <Icon :icon="feature.icon" class="text-3xl text-neon" />
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">{{ feature.title }}</h3>
                <p class="text-gray-400">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Medical Disclaimer -->
        <div class="mt-12 max-w-4xl mx-auto bg-orange-500/10 border border-orange-500/30 rounded-2xl p-6">
          <div class="flex items-start gap-4">
            <Icon icon="hugeicons:alert-02" class="text-2xl text-orange-400 flex-shrink-0 mt-1" />
            <div>
              <h4 class="font-bold text-orange-400 mb-2">Важное предупреждение</h4>
              <p class="text-gray-400 text-sm">
                MuscleUp Vision является инструментом для самостоятельных тренировок и не заменяет профессиональную медицинскую консультацию.
                Перед началом любой программы тренировок рекомендуется проконсультироваться с врачом, особенно при наличии хронических заболеваний,
                травм или противопоказаний к физическим нагрузкам. Пользователь принимает на себя ответственность за своё здоровье при использовании приложения.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Roadmap Section -->
    <section id="roadmap" class="roadmap-section py-32 relative">
      <div class="absolute inset-0 bg-gradient-to-b from-transparent via-neon/5 to-transparent"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            <span class="text-neon">Roadmap</span> развития
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Наши планы на ближайшее будущее
          </p>
        </div>

        <!-- Timeline -->
        <div class="max-w-5xl mx-auto">
          <div class="grid md:grid-cols-4 gap-6">
            <div
              v-for="(item, index) in roadmapItems"
              :key="index"
              class="relative"
            >
              <!-- Connector line -->
              <div v-if="Number(index) < roadmapItems.length - 1" class="hidden md:block absolute top-8 left-full w-6 h-0.5 bg-white/10"></div>

              <div
                class="bg-[#111] rounded-3xl p-6 border transition-all duration-300 h-full"
                :class="item.status === 'current' ? 'border-neon/50 shadow-[0_0_30px_rgba(204,255,0,0.1)]' : 'border-white/5'"
              >
                <!-- Status Badge -->
                <div
                  class="inline-block px-3 py-1 rounded-full text-xs font-medium mb-4"
                  :class="{
                    'bg-neon text-black': item.status === 'current',
                    'bg-blue-500/20 text-blue-400': item.status === 'upcoming',
                    'bg-white/10 text-gray-400': item.status === 'planned'
                  }"
                >
                  {{ item.quarter }}
                </div>

                <h3 class="text-lg font-bold mb-4">{{ item.title }}</h3>

                <ul class="space-y-2">
                  <li
                    v-for="(feature, idx) in item.items"
                    :key="idx"
                    class="flex items-start gap-2 text-sm text-gray-400"
                  >
                    <Icon
                      :icon="item.status === 'current' ? 'hugeicons:checkmark-circle-02' : 'hugeicons:circle'"
                      :class="item.status === 'current' ? 'text-neon' : 'text-gray-600'"
                      class="mt-0.5 flex-shrink-0"
                    />
                    <span>{{ feature }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Competitive Advantage Section -->
    <section class="comparison-section py-32 relative">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Почему <span class="text-neon">мы лучше</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-2xl mx-auto">
            Сравнение с конкурентами
          </p>
        </div>

        <!-- Comparison Table -->
        <div class="max-w-5xl mx-auto overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-white/10">
                <th class="text-left py-4 px-4 text-gray-400 font-medium">Приложение</th>
                <th class="text-center py-4 px-4 text-gray-400 font-medium">Real-time Pose</th>
                <th class="text-center py-4 px-4 text-gray-400 font-medium">Без оборудования</th>
                <th class="text-center py-4 px-4 text-gray-400 font-medium">AI Планы</th>
                <th class="text-center py-4 px-4 text-gray-400 font-medium">Коррекция формы</th>
                <th class="text-center py-4 px-4 text-gray-400 font-medium">Бесплатно</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(competitor, index) in competitors"
                :key="index"
                class="border-b border-white/5"
                :class="index === 0 ? 'bg-neon/5' : ''"
              >
                <td class="py-4 px-4 font-medium" :class="index === 0 ? 'text-neon' : 'text-white'">
                  {{ competitor.name }}
                </td>
                <td class="text-center py-4 px-4">
                  <Icon
                    :icon="competitor.realTimePose ? 'hugeicons:checkmark-circle-02' : 'hugeicons:cancel-circle'"
                    :class="competitor.realTimePose ? 'text-green-500' : 'text-red-500/50'"
                    class="text-xl"
                  />
                </td>
                <td class="text-center py-4 px-4">
                  <Icon
                    :icon="competitor.noHardware ? 'hugeicons:checkmark-circle-02' : 'hugeicons:cancel-circle'"
                    :class="competitor.noHardware ? 'text-green-500' : 'text-red-500/50'"
                    class="text-xl"
                  />
                </td>
                <td class="text-center py-4 px-4">
                  <Icon
                    :icon="competitor.aiPlans ? 'hugeicons:checkmark-circle-02' : 'hugeicons:cancel-circle'"
                    :class="competitor.aiPlans ? 'text-green-500' : 'text-red-500/50'"
                    class="text-xl"
                  />
                </td>
                <td class="text-center py-4 px-4">
                  <Icon
                    :icon="competitor.formCorrection ? 'hugeicons:checkmark-circle-02' : 'hugeicons:cancel-circle'"
                    :class="competitor.formCorrection ? 'text-green-500' : 'text-red-500/50'"
                    class="text-xl"
                  />
                </td>
                <td class="text-center py-4 px-4">
                  <Icon
                    :icon="competitor.free ? 'hugeicons:checkmark-circle-02' : 'hugeicons:cancel-circle'"
                    :class="competitor.free ? 'text-green-500' : 'text-red-500/50'"
                    class="text-xl"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section id="faq" class="faq-section py-32 relative">
      <div class="absolute inset-0 bg-gradient-to-b from-neon/5 via-transparent to-neon/5"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Частые <span class="text-neon">вопросы</span>
          </h2>
        </div>

        <div class="max-w-3xl mx-auto space-y-4">
          <div
            v-for="(item, index) in faqItems"
            :key="index"
            class="bg-[#111] rounded-2xl border border-white/5 overflow-hidden"
          >
            <details class="group">
              <summary class="flex items-center justify-between p-6 cursor-pointer list-none">
                <h3 class="font-bold text-lg pr-4">{{ item.question }}</h3>
                <Icon
                  icon="hugeicons:arrow-down-01"
                  class="text-xl text-neon flex-shrink-0 transition-transform group-open:rotate-180"
                />
              </summary>
              <div class="px-6 pb-6 text-gray-400">
                {{ item.answer }}
              </div>
            </details>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="team-section py-32 relative">
      <!-- Background Effect -->
      <div class="absolute inset-0 bg-gradient-to-b from-neon/5 via-transparent to-neon/5"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-4xl md:text-6xl font-bold">
            Команда <span class="text-neon">MuscleUp</span>
          </h2>
          <p class="text-xl text-gray-400 max-w-3xl mx-auto">
            Успех MuscleUp обеспечивается опытной командой специалистов с сильным бэкграундом в ИИ, мобильной разработке и стартапах
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          <div
            v-for="(member, index) in team"
            :key="index"
            class="team-card group bg-gradient-to-br from-card to-card-hover rounded-3xl p-8 border border-white/5 hover:border-neon/50 transition-all duration-300 hover:shadow-neon-card"
          >
            <!-- Avatar & Role -->
            <div class="text-center mb-6">
              <div class="w-24 h-24 mx-auto mb-4 rounded-2xl overflow-hidden group-hover:ring-2 group-hover:ring-neon/50 transition-all duration-300">
                <img
                  v-if="member.avatar"
                  :src="member.avatar"
                  :alt="member.name"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full bg-neon/10 flex items-center justify-center text-5xl group-hover:bg-neon/20 transition-all duration-300">
                  {{ member.name.charAt(0) }}
                </div>
              </div>
              <h3 class="text-2xl font-bold mb-1">{{ member.name }}</h3>
              <p class="text-neon font-semibold text-sm">{{ member.role }}</p>
            </div>

            <!-- Education & Experience -->
            <div class="space-y-4 mb-6">
              <div class="space-y-2">
                <div class="flex items-start gap-2">
                  <Icon icon="hugeicons:mortarboard-02" class="text-neon text-lg mt-0.5 flex-shrink-0" />
                  <p class="text-sm text-gray-400">{{ member.education }}</p>
                </div>
                <div class="flex items-start gap-2">
                  <Icon icon="hugeicons:briefcase-02" class="text-neon text-lg mt-0.5 flex-shrink-0" />
                  <p class="text-sm text-gray-400">{{ member.experience }}</p>
                </div>
              </div>

              <!-- Responsibilities -->
              <div class="space-y-2">
                <div class="flex items-center gap-2 mb-2">
                  <Icon icon="hugeicons:check-list" class="text-neon text-lg" />
                  <span class="text-xs font-semibold text-gray-500 uppercase">Роль в проекте</span>
                </div>
                <ul class="space-y-1.5 ml-6">
                  <li v-for="(resp, idx) in member.responsibilities" :key="idx" class="text-xs text-gray-400 flex items-start gap-2">
                    <span class="text-neon mt-1">•</span>
                    <span>{{ resp }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Social Links -->
            <div class="flex gap-3 pt-4 border-t border-white/5">
              <a
                v-if="member.social.linkedin"
                :href="member.social.linkedin"
                target="_blank"
                class="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-white/5 hover:bg-neon/10 rounded-xl transition-all duration-300 text-sm"
              >
                <Icon icon="hugeicons:linkedin-02" class="text-lg" />
                <span>LinkedIn</span>
              </a>
              <a
                v-if="member.social.github"
                :href="member.social.github"
                target="_blank"
                class="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-white/5 hover:bg-neon/10 rounded-xl transition-all duration-300 text-sm"
              >
                <Icon icon="hugeicons:github" class="text-lg" />
                <span>GitHub</span>
              </a>
            </div>
          </div>
        </div>

        <!-- Team Stats -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto mt-16">
          <div class="text-center p-6 bg-card rounded-2xl border border-white/5">
            <div class="text-3xl font-bold text-neon mb-2">3</div>
            <div class="text-sm text-gray-400">Члена команды</div>
          </div>
          <div class="text-center p-6 bg-card rounded-2xl border border-white/5">
            <div class="text-3xl font-bold text-neon mb-2">50k+</div>
            <div class="text-sm text-gray-400">Пользователей</div>
          </div>
          <div class="text-center p-6 bg-card rounded-2xl border border-white/5">
            <div class="text-3xl font-bold text-neon mb-2">5+</div>
            <div class="text-sm text-gray-400">Проектов запущено</div>
          </div>
          <div class="text-center p-6 bg-card rounded-2xl border border-white/5">
            <div class="text-3xl font-bold text-neon mb-2">100%</div>
            <div class="text-sm text-gray-400">Преданность делу</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-32 relative overflow-hidden">
      <!-- Background Effects -->
      <div class="absolute inset-0 bg-gradient-radial from-neon/10 via-transparent to-transparent"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-neon/5 rounded-full blur-[150px]"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="max-w-4xl mx-auto text-center space-y-8">
          <h2 class="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight">
            Начните тренироваться <br />
            <span class="text-neon glow-text">правильно сегодня</span>
          </h2>

          <p class="text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto">
            Присоединяйтесь к революции в фитнесе. Персональный ИИ-тренер всегда с вами.
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <NuxtLink to="https://app.muscleup.fitness/"
              class="group px-10 py-5 bg-neon text-black font-bold text-xl rounded-2xl hover:brightness-110 transition-all duration-300 shadow-neon-lg hover:shadow-neon-xl flex items-center gap-3"
            >
              Начать тренировку
              <Icon icon="hugeicons:arrow-right-02" class="text-2xl group-hover:translate-x-1 transition-transform" />
          </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-16 border-t border-white/5">
      <div class="container mx-auto px-6">
        <div class="grid md:grid-cols-4 gap-12 mb-12">
          <!-- Brand -->
          <div class="md:col-span-2">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 rounded-xl bg-neon flex items-center justify-center">
                <Icon icon="hugeicons:workout-run" class="text-2xl text-black" />
              </div>
              <span class="text-xl font-bold">MuscleUp Vision</span>
            </div>
            <p class="text-gray-400 text-sm mb-4 max-w-md">
              AI-powered fitness platform that uses computer vision to analyze your exercise form in real-time.
              Train smarter, not harder.
            </p>
            <div class="flex gap-4">
              <a href="https://github.com/themilan1337/aitucup" target="_blank" class="text-gray-400 hover:text-neon transition">
                <Icon icon="hugeicons:github" class="text-2xl" />
              </a>
              <a href="https://linkedin.com" target="_blank" class="text-gray-400 hover:text-neon transition">
                <Icon icon="hugeicons:linkedin-02" class="text-2xl" />
              </a>
            </div>
          </div>

          <!-- Quick Links -->
          <div>
            <h4 class="font-bold mb-4">Навигация</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#how-it-works" class="hover:text-neon transition">Как это работает</a></li>
              <li><a href="#demo" class="hover:text-neon transition">Демо</a></li>
              <li><a href="#technology" class="hover:text-neon transition">Технологии</a></li>
              <li><a href="#roadmap" class="hover:text-neon transition">Roadmap</a></li>
              <li><a href="#faq" class="hover:text-neon transition">FAQ</a></li>
            </ul>
          </div>

          <!-- Legal -->
          <div>
            <h4 class="font-bold mb-4">Правовая информация</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#privacy" class="hover:text-neon transition">Privacy Policy</a></li>
              <li><a href="#privacy" class="hover:text-neon transition">Terms of Service</a></li>
              <li><a href="#privacy" class="hover:text-neon transition">Medical Disclaimer</a></li>
            </ul>
          </div>
        </div>

        <div class="border-t border-white/5 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p class="text-sm text-gray-500">
            © 2026 MuscleUp Vision. AITU CAP Project.
          </p>
          <p class="text-sm text-gray-500">
            Made with 💚 by Milan, Bizhan and Sultan
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Custom CSS Variables */
:root {
  --color-neon: #ccff00;
  --color-bg: #000000;
  --color-card: #111111;
  --color-card-hover: #1a1a1a;
}

/* Glow Effects */
.glow-text {
  text-shadow: 0 0 20px rgba(204, 255, 0, 0.3),
               0 0 40px rgba(204, 255, 0, 0.2),
               0 0 60px rgba(204, 255, 0, 0.1);
}

.shadow-neon {
  box-shadow: 0 0 20px rgba(204, 255, 0, 0.3),
              0 0 40px rgba(204, 255, 0, 0.2);
}

.shadow-neon-lg {
  box-shadow: 0 0 30px rgba(204, 255, 0, 0.4),
              0 0 60px rgba(204, 255, 0, 0.3),
              0 10px 80px rgba(204, 255, 0, 0.2);
}

.shadow-neon-xl {
  box-shadow: 0 0 40px rgba(204, 255, 0, 0.5),
              0 0 80px rgba(204, 255, 0, 0.4),
              0 10px 100px rgba(204, 255, 0, 0.3);
}

.shadow-neon-card {
  box-shadow: 0 0 20px rgba(204, 255, 0, 0.1),
              0 10px 40px rgba(0, 0, 0, 0.5);
}

/* Gradient utilities */
.bg-gradient-radial {
  background: radial-gradient(circle, var(--tw-gradient-stops));
}

/* Tailwind color utilities */
.text-neon {
  color: var(--color-neon);
}

.bg-neon {
  background-color: var(--color-neon);
}

.bg-card {
  background-color: var(--color-card);
}

.bg-card-hover {
  background-color: var(--color-card-hover);
}

.border-neon {
  border-color: var(--color-neon);
}
</style>
