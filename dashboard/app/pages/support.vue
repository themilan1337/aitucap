<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Expanded FAQ sections
const expandedSections = ref<Set<number>>(new Set())

// FAQ data
const faqSections = [
  {
    title: 'Начало работы',
    questions: [
      {
        q: 'Как начать тренироваться?',
        a: 'После регистрации пройдите короткую анкету о ваших целях и уровне подготовки. Приложение автоматически создаст персональный план тренировок на 30 дней.'
      },
      {
        q: 'Нужно ли специальное оборудование?',
        a: 'Нет! Все упражнения можно выполнять с собственным весом тела. Дополнительное оборудование опционально и может быть указано в настройках профиля.'
      },
      {
        q: 'Как работает отслеживание упражнений?',
        a: 'Приложение использует камеру вашего устройства и технологию компьютерного зрения для отслеживания движений в реальном времени. Искусственный интеллект анализирует вашу технику и считает повторения автоматически.'
      }
    ]
  },
  {
    title: 'Тренировки',
    questions: [
      {
        q: 'Можно ли изменить план тренировок?',
        a: 'Да! Вы можете в любой момент перегенерировать план в разделе "План" или изменить настройки профиля для адаптации тренировок под ваши нужды.'
      },
      {
        q: 'Что делать, если упражнение слишком сложное?',
        a: 'Вы можете пропустить упражнение или изменить уровень сложности в настройках профиля. Приложение подберет более подходящие варианты.'
      },
      {
        q: 'Как правильно настроить камеру?',
        a: 'Установите устройство на расстоянии 1.5-2 метра так, чтобы вы полностью помещались в кадр. Используйте хорошее освещение и убедитесь, что фон контрастный.'
      }
    ]
  },
  {
    title: 'Точность и техника',
    questions: [
      {
        q: 'Почему не засчитываются повторения?',
        a: 'Убедитесь, что вы выполняете упражнение правильно - с полной амплитудой движения. Проверьте настройки камеры и убедитесь, что ваше тело полностью видно в кадре.'
      },
      {
        q: 'Как улучшить точность распознавания?',
        a: 'Используйте хорошее освещение, носите контрастную одежду, убедитесь что вся фигура видна в кадре. Настройте порог уверенности в настройках камеры.'
      },
      {
        q: 'Что означают подсказки по технике?',
        a: 'Приложение анализирует вашу форму выполнения и дает рекомендации в реальном времени. Следуйте этим советам для безопасного и эффективного выполнения упражнений.'
      }
    ]
  },
  {
    title: 'Учетная запись и данные',
    questions: [
      {
        q: 'Как изменить личные данные?',
        a: 'Перейдите в Профиль → Личные данные. Здесь вы можете обновить вес, рост, цели и другие параметры для более точной персонализации.'
      },
      {
        q: 'Безопасны ли мои данные?',
        a: 'Да! Все данные хранятся в зашифрованном виде. Видео с камеры обрабатывается локально на вашем устройстве и не передается на серверы.'
      },
      {
        q: 'Как удалить аккаунт?',
        a: 'Напишите нам на support@aitucup.com с указанием вашего email. Мы удалим все ваши данные в течение 48 часов.'
      }
    ]
  }
]

const toggleSection = (index: number) => {
  if (expandedSections.value.has(index)) {
    expandedSections.value.delete(index)
  } else {
    expandedSections.value.add(index)
  }
}

// Contact form
const contactForm = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const isSubmitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref('')

const handleSubmit = async () => {
  isSubmitting.value = true
  submitError.value = ''
  submitSuccess.value = false

  // Simulate form submission
  await new Promise(resolve => setTimeout(resolve, 1000))

  // Here you would normally send to backend
  console.log('Contact form submitted:', contactForm.value)

  isSubmitting.value = false
  submitSuccess.value = true

  // Reset form
  setTimeout(() => {
    contactForm.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    }
    submitSuccess.value = false
  }, 3000)
}
</script>

<template>
  <div class="px-4 pt-12 pb-24">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <button @click="router.push('/profile')" class="text-gray-400 hover:text-white">
        <Icon icon="heroicons:arrow-left" class="text-2xl" />
      </button>
      <h1 class="text-3xl font-bold">Помощь и поддержка</h1>
    </div>

    <!-- Quick Help Cards -->
    <div class="grid grid-cols-2 gap-4 mb-8">
      <a href="mailto:support@aitucup.com" class="bg-[#1A1A1A] rounded-2xl p-4 hover:bg-[#222] transition-colors">
        <div class="flex flex-col items-center text-center gap-2">
          <div class="w-12 h-12 bg-neon/20 rounded-full flex items-center justify-center">
            <Icon icon="heroicons:envelope" class="text-neon text-2xl" />
          </div>
          <span class="font-semibold">Email</span>
          <span class="text-xs text-gray-400">support@aitucup.com</span>
        </div>
      </a>

      <a href="https://t.me/aitucup" target="_blank" class="bg-[#1A1A1A] rounded-2xl p-4 hover:bg-[#222] transition-colors">
        <div class="flex flex-col items-center text-center gap-2">
          <div class="w-12 h-12 bg-neon/20 rounded-full flex items-center justify-center">
            <Icon icon="simple-icons:telegram" class="text-neon text-2xl" />
          </div>
          <span class="font-semibold">Telegram</span>
          <span class="text-xs text-gray-400">@aitucup</span>
        </div>
      </a>
    </div>

    <!-- FAQ Sections -->
    <div class="mb-8">
      <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
        <Icon icon="heroicons:question-mark-circle" class="text-neon" />
        Часто задаваемые вопросы
      </h2>

      <div class="space-y-3">
        <div v-for="(section, sectionIndex) in faqSections" :key="sectionIndex" class="bg-[#1A1A1A] rounded-2xl overflow-hidden">
          <button
            @click="toggleSection(sectionIndex)"
            class="w-full flex items-center justify-between p-4 hover:bg-[#222] transition-colors"
          >
            <h3 class="font-semibold text-left">{{ section.title }}</h3>
            <Icon
              :icon="expandedSections.has(sectionIndex) ? 'heroicons:chevron-up' : 'heroicons:chevron-down'"
              class="text-gray-400 text-xl transition-transform"
            />
          </button>

          <div
            v-if="expandedSections.has(sectionIndex)"
            class="border-t border-white/5"
          >
            <div v-for="(item, itemIndex) in section.questions" :key="itemIndex" class="border-b border-white/5 last:border-0">
              <details class="group">
                <summary class="p-4 cursor-pointer hover:bg-[#111] transition-colors list-none">
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-gray-300">{{ item.q }}</span>
                    <Icon icon="heroicons:plus" class="text-gray-500 text-lg group-open:rotate-45 transition-transform" />
                  </div>
                </summary>
                <div class="px-4 pb-4 text-sm text-gray-400">
                  {{ item.a }}
                </div>
              </details>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Form -->
    <div class="bg-[#1A1A1A] rounded-2xl p-4">
      <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
        <Icon icon="heroicons:paper-airplane" class="text-neon" />
        Свяжитесь с нами
      </h2>

      <!-- Success Message -->
      <div v-if="submitSuccess" class="bg-green-500/20 border border-green-500 text-green-500 px-4 py-3 rounded-xl mb-4">
        <div class="flex items-center gap-2">
          <Icon icon="heroicons:check-circle" class="text-xl" />
          <span>Сообщение отправлено! Мы свяжемся с вами в ближайшее время.</span>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="submitError" class="bg-red-500/20 border border-red-500 text-red-500 px-4 py-3 rounded-xl mb-4">
        <div class="flex items-center gap-2">
          <Icon icon="heroicons:exclamation-circle" class="text-xl" />
          <span>{{ submitError }}</span>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm text-gray-400 mb-2">Имя</label>
          <input
            v-model="contactForm.name"
            type="text"
            required
            class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            placeholder="Ваше имя"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400 mb-2">Email</label>
          <input
            v-model="contactForm.email"
            type="email"
            required
            class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            placeholder="your@email.com"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400 mb-2">Тема</label>
          <input
            v-model="contactForm.subject"
            type="text"
            required
            class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon"
            placeholder="Кратко о проблеме"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400 mb-2">Сообщение</label>
          <textarea
            v-model="contactForm.message"
            required
            rows="5"
            class="w-full bg-[#111] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon resize-none"
            placeholder="Опишите вашу проблему или вопрос подробнее..."
          ></textarea>
        </div>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-neon text-black py-4 rounded-xl font-semibold hover:brightness-110 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <svg v-if="isSubmitting" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <Icon v-else icon="heroicons:paper-airplane" class="text-xl" />
          <span>{{ isSubmitting ? 'Отправка...' : 'Отправить' }}</span>
        </button>
      </form>
    </div>

    <!-- Additional Resources -->
    <div class="mt-6 bg-neon/10 border border-neon/20 rounded-2xl p-4">
      <div class="flex items-start gap-3">
        <Icon icon="heroicons:light-bulb" class="text-neon text-2xl flex-shrink-0 mt-1" />
        <div>
          <h3 class="font-semibold mb-1">Совет</h3>
          <p class="text-sm text-gray-400">
            Для быстрого ответа отправьте сообщение в Telegram или проверьте раздел FAQ выше. Мы отвечаем на письма в течение 24 часов.
          </p>
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
