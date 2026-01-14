import { defineStore } from 'pinia'

export interface Exercise {
  id: string
  name: string
  sets: number
  reps: number
  duration?: number // in minutes
  muscleGroup?: string
  completed: boolean
}

export interface WorkoutExercise {
  name: string
  reps: number
  icon: string
}

export interface WorkoutHistory {
  date: string // e.g., '11 января'
  exercises: WorkoutExercise[]
  calories: number
  duration: string // e.g., '4:09'
  accuracy: number
  completed: boolean
}

export interface Achievement {
  id: string
  name: string
  icon: string
  unlocked: boolean
  description?: string
}

export interface TrainingStoreState {
  streak: number
  todayExercises: Exercise[]
  weeklyStats: {
    workouts: number
    calories: number
    minutes: number
  }
  lifetimeStats: {
    totalWorkouts: number
    totalReps: number
    avgAccuracy: number
    bestStreak: number
  }
  progressData: {
    accuracyTrend: number[]
    weeklyFrequency: number[]
  }
  records: {
    squats: number
    lunges: number
    pushups: number
    plank: number // seconds
  }
  workoutHistory: WorkoutHistory[]
  achievements: Achievement[]
}

export const useTrainingStore = defineStore('training', {
  state: (): TrainingStoreState => ({
    streak: 19,
    todayExercises: [
      { id: '1', name: 'Приседания', sets: 3, reps: 20, muscleGroup: 'Ноги', completed: false },
      { id: '2', name: 'Выпады', sets: 3, reps: 15, muscleGroup: 'Ноги', completed: false },
    ],
    weeklyStats: {
      workouts: 4,
      calories: 111,
      minutes: 50,
    },
    lifetimeStats: {
      totalWorkouts: 19,
      totalReps: 908,
      avgAccuracy: 86,
      bestStreak: 3,
    },
    progressData: {
      // Mock data points for the trend chart
      accuracyTrend: [82, 85, 83, 86, 88, 87, 86, 89, 90, 88, 87, 86, 88, 89],
      // Mock data for weekly bar chart (Mon-Sun)
      weeklyFrequency: [1, 1, 1, 0, 1, 0, 0], // 1 = trained, 0 = rest
    },
    records: {
      squats: 28,
      lunges: 40,
      pushups: 22,
      plank: 1, // '1 сек' in screenshot? likely placeholder, but keeping type consistent
    },
    workoutHistory: [
      {
        date: '11 января',
        exercises: [
          { name: 'Выпады', reps: 40, icon: 'heroicons:bolt' },
          { name: 'Приседания', reps: 28, icon: 'heroicons:bolt' },
          { name: 'Планка', reps: 1, icon: 'heroicons:bolt' },
        ],
        calories: 45,
        duration: '4:09',
        accuracy: 86,
        completed: true,
      },
      {
        date: '10 января',
        exercises: [
          { name: 'Приседания', reps: 15, icon: 'heroicons:bolt' },
          { name: 'Планка', reps: 1, icon: 'heroicons:bolt' },
          { name: 'Отжимания', reps: 17, icon: 'heroicons:bolt' },
        ],
        calories: 25,
        duration: '2:46',
        accuracy: 88,
        completed: true,
      },
      {
        date: '8 января',
        exercises: [
          { name: 'Приседания', reps: 19, icon: 'heroicons:bolt' },
          { name: 'Отжимания', reps: 20, icon: 'heroicons:bolt' },
        ],
        calories: 23,
        duration: '1:57',
        accuracy: 88,
        completed: true,
      },
    ],
    achievements: [
      { id: '1', name: 'Первая тренировка', icon: 'heroicons:star', unlocked: true, description: 'Завершите первую тренировку' },
      { id: '2', name: 'Серия 7 дней', icon: 'heroicons:fire', unlocked: true, description: 'Тренируйтесь 7 дней подряд' },
      { id: '3', name: '100 повторений', icon: 'heroicons:trophy', unlocked: false, description: 'Выполните 100 повторений' },
      { id: '4', name: 'Мастер формы', icon: 'heroicons:check-badge', unlocked: true, description: 'Достигните точности 90%' },
      { id: '5', name: '20 тренировок', icon: 'heroicons:calendar', unlocked: false, description: 'Завершите 20 тренировок' },
      { id: '6', name: 'Серия 30 дней', icon: 'heroicons:bolt', unlocked: false, description: 'Тренируйтесь 30 дней подряд' },
    ],
  }),
  actions: {
    toggleExerciseCompletion(id: string) {
      const ex = this.todayExercises.find((e) => e.id === id)
      if (ex) {
        ex.completed = !ex.completed
      }
    }
  },
  persist: true,
})
