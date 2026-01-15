<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ref, onMounted, onUnmounted } from 'vue'

// Intersection Observer for scroll animations
const heroRef = ref<HTMLElement | null>(null)
const featuresRef = ref<HTMLElement | null>(null)
const howItWorksRef = ref<HTMLElement | null>(null)
const benefitsRef = ref<HTMLElement | null>(null)
const ctaRef = ref<HTMLElement | null>(null)

const isVisible = ref({
  hero: false,
  features: false,
  howItWorks: false,
  benefits: false,
  cta: false,
})

let observer: IntersectionObserver | null = null

onMounted(() => {
  // Smooth scroll behavior
  document.documentElement.style.scrollBehavior = 'smooth'

  // Setup intersection observer for animations
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const target = entry.target as HTMLElement
          const key = target.dataset.section as keyof typeof isVisible.value
          if (key) {
            isVisible.value[key] = true
          }
        }
      })
    },
    { threshold: 0.1 }
  )

  // Observe sections
  if (heroRef.value) observer.observe(heroRef.value)
  if (featuresRef.value) observer.observe(featuresRef.value)
  if (howItWorksRef.value) observer.observe(howItWorksRef.value)
  if (benefitsRef.value) observer.observe(benefitsRef.value)
  if (ctaRef.value) observer.observe(ctaRef.value)

  // Parallax effect
  window.addEventListener('scroll', handleParallax)
})

onUnmounted(() => {
  if (observer) observer.disconnect()
  window.removeEventListener('scroll', handleParallax)
})

const handleParallax = () => {
  const scrolled = window.scrollY
  const parallaxElements = document.querySelectorAll('.parallax')
  parallaxElements.forEach((el) => {
    const speed = parseFloat((el as HTMLElement).dataset.speed || '0.5')
    const yPos = -(scrolled * speed)
    ;(el as HTMLElement).style.transform = `translateY(${yPos}px)`
  })
}

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
</script>

<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section
      ref="heroRef"
      data-section="hero"
      class="hero-section relative min-h-screen flex items-center justify-center overflow-hidden"
      :class="{ 'animate-in': isVisible.hero }"
    >
      <!-- Background Effects -->
      <div class="absolute inset-0 bg-gradient-radial from-neon/5 via-transparent to-transparent opacity-50"></div>
      <div class="absolute top-20 left-1/4 w-96 h-96 bg-neon/10 rounded-full blur-[120px] animate-pulse-slow parallax" data-speed="0.3"></div>
      <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-neon/5 rounded-full blur-[100px] animate-pulse-slow" style="animation-delay: 1s"></div>

      <div class="container mx-auto px-6 py-20 relative z-10">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Text Content -->
          <div class="hero-content space-y-8">
            <div class="space-y-4 animate-slide-up" style="animation-delay: 0.1s">
              <div class="inline-block px-4 py-2 bg-neon/10 border border-neon/30 rounded-full text-neon text-sm font-medium backdrop-blur-sm">
                AITU CUP 2024
              </div>
              <h1 class="text-5xl md:text-7xl font-bold leading-tight">
                Тренируйтесь <br />
                <span class="text-neon glow-text">правильно</span> с <br />
                помощью ИИ
              </h1>
            </div>

            <p class="text-xl text-gray-400 max-w-xl animate-slide-up" style="animation-delay: 0.2s">
              MuscleUp Vision использует компьютерное зрение для анализа техники упражнений.
              Тренируйтесь безопасно и эффективно с персональным ИИ-тренером.
            </p>

            <div class="flex flex-col sm:flex-row gap-4 animate-slide-up" style="animation-delay: 0.3s">
              <a
                href="http://localhost:3001"
                class="group px-8 py-4 bg-neon text-black font-bold text-lg rounded-2xl hover:brightness-110 active:scale-[0.98] transition-all duration-300 shadow-neon hover:shadow-neon-lg flex items-center justify-center gap-3"
              >
                Начать тренировку
                <Icon icon="hugeicons:arrow-right-02" class="text-2xl group-hover:translate-x-1 transition-transform" />
              </a>
              <a
                href="#how-it-works"
                class="px-8 py-4 bg-white/5 border border-white/10 text-white font-bold text-lg rounded-2xl hover:bg-white/10 hover:border-neon/50 active:scale-[0.98] transition-all duration-300 backdrop-blur-sm flex items-center justify-center gap-3"
              >
                Как это работает
                <Icon icon="hugeicons:arrow-down-01" class="text-2xl" />
              </a>
            </div>

            <!-- Stats -->
            <div class="flex gap-8 pt-8 animate-slide-up" style="animation-delay: 0.4s">
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
          <div class="relative animate-slide-up" style="animation-delay: 0.2s">
            <div class="absolute inset-0 bg-gradient-to-t from-neon/20 via-transparent to-transparent rounded-3xl blur-2xl"></div>
            <div class="relative parallax" data-speed="0.2">
              <img
                src="/girl.png"
                alt="MuscleUp Vision AI Fitness"
                class="w-full h-auto drop-shadow-2xl animate-float"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce">
        <Icon icon="hugeicons:arrow-down-01" class="text-3xl text-neon/50" />
      </div>
    </section>

    <!-- Features Section -->
    <section
      ref="featuresRef"
      data-section="features"
      class="features-section py-32 relative"
      :class="{ 'animate-in': isVisible.features }"
    >
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
            class="feature-card group bg-card rounded-3xl p-8 hover:bg-card-hover transition-all duration-500 border border-white/5 hover:border-neon/50 hover:shadow-neon-card animate-slide-up"
            :style="{ 'animation-delay': `${index * 0.1}s` }"
          >
            <div class="w-16 h-16 rounded-2xl bg-neon/10 flex items-center justify-center mb-6 group-hover:bg-neon/20 group-hover:scale-110 transition-all duration-500">
              <Icon :icon="feature.icon" class="text-4xl text-neon" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ feature.title }}</h3>
            <p class="text-gray-400 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section
      id="how-it-works"
      ref="howItWorksRef"
      data-section="howItWorks"
      class="how-it-works-section py-32 relative"
      :class="{ 'animate-in': isVisible.howItWorks }"
    >
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
            <!-- Connection Line -->
            <div
              v-if="index < steps.length - 1"
              class="hidden md:block absolute left-16 top-32 w-0.5 h-20 bg-gradient-to-b from-neon/50 to-transparent"
            ></div>

            <div
              class="flex flex-col md:flex-row gap-8 items-start md:items-center bg-card rounded-3xl p-8 border border-white/5 hover:border-neon/30 transition-all duration-500 hover:shadow-neon-card animate-slide-up"
              :style="{ 'animation-delay': `${index * 0.15}s` }"
            >
              <!-- Step Number -->
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
    <section
      ref="benefitsRef"
      data-section="benefits"
      class="benefits-section py-32 relative"
      :class="{ 'animate-in': isVisible.benefits }"
    >
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
            class="benefit-card group bg-gradient-to-br from-card to-card-hover rounded-3xl p-10 border border-white/5 hover:border-neon/50 transition-all duration-500 hover:shadow-neon-card animate-slide-up"
            :style="{ 'animation-delay': `${index * 0.1}s` }"
          >
            <div class="flex items-start gap-6">
              <div class="w-20 h-20 rounded-2xl bg-neon/10 flex items-center justify-center flex-shrink-0 group-hover:bg-neon/20 group-hover:scale-110 transition-all duration-500">
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

    <!-- CTA Section -->
    <section
      ref="ctaRef"
      data-section="cta"
      class="cta-section py-32 relative overflow-hidden"
      :class="{ 'animate-in': isVisible.cta }"
    >
      <!-- Background Effects -->
      <div class="absolute inset-0 bg-gradient-radial from-neon/10 via-transparent to-transparent"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-neon/5 rounded-full blur-[150px] animate-pulse-slow"></div>

      <div class="container mx-auto px-6 relative z-10">
        <div class="max-w-4xl mx-auto text-center space-y-8">
          <h2 class="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight animate-slide-up">
            Начните тренироваться <br />
            <span class="text-neon glow-text">правильно сегодня</span>
          </h2>

          <p class="text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto animate-slide-up" style="animation-delay: 0.1s">
            Присоединяйтесь к революции в фитнесе. Персональный ИИ-тренер всегда с вами.
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center animate-slide-up" style="animation-delay: 0.2s">
            <a
              href="http://localhost:3001"
              class="group px-10 py-5 bg-neon text-black font-bold text-xl rounded-2xl hover:brightness-110 active:scale-[0.98] transition-all duration-300 shadow-neon-lg hover:shadow-neon-xl flex items-center gap-3"
            >
              Начать тренировку
              <Icon icon="hugeicons:arrow-right-02" class="text-2xl group-hover:translate-x-1 transition-transform" />
            </a>
          </div>

          <!-- Additional Info -->
          <div class="flex flex-wrap justify-center gap-8 pt-12 text-gray-500 animate-slide-up" style="animation-delay: 0.3s">
            <div class="flex items-center gap-2">
              <Icon icon="hugeicons:checkmark-circle-01" class="text-xl text-neon" />
              <span>Бесплатно навсегда</span>
            </div>
            <div class="flex items-center gap-2">
              <Icon icon="hugeicons:shield-check" class="text-xl text-neon" />
              <span>Безопасно и конфиденциально</span>
            </div>
            <div class="flex items-center gap-2">
              <Icon icon="hugeicons:ai-brain-01" class="text-xl text-neon" />
              <span>Технология будущего</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 border-t border-white/5">
      <div class="container mx-auto px-6">
        <div class="flex flex-col md:flex-row justify-between items-center gap-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-neon flex items-center justify-center">
              <Icon icon="hugeicons:workout-run" class="text-2xl text-black" />
            </div>
            <span class="text-xl font-bold">MuscleUp Vision</span>
          </div>

          <div class="text-center md:text-right text-gray-500">
            <p>© 2024 AITU CUP. Создано с помощью ИИ.</p>
          </div>
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

/* Animations */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}

.animate-slide-up {
  animation: slide-up 0.8s ease-out forwards;
  opacity: 0;
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Section animations */
.animate-in .animate-slide-up {
  animation: slide-up 0.8s ease-out forwards;
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

/* Smooth transitions */
* {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
