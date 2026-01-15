/**
 * Workout History Composable
 * Handles fetching workout history and saving completed workouts
 */

export interface ExercisePerformance {
  exercise_type: string
  reps: number
  duration: number
  form_accuracy: number
  form_corrections: string[]
  calories_burned: number
  order_index: number
}

export interface WorkoutSession {
  id: string
  user_id: string
  plan_day_id?: string
  started_at: string
  completed_at: string
  total_duration: number
  total_calories: number
  average_form_accuracy: number
  exercises: ExercisePerformance[]
}

export interface WorkoutSessionCreate {
  plan_day_id?: string
  started_at: string
  completed_at: string
  total_duration: number
  total_calories: number
  average_form_accuracy: number
  exercises: ExercisePerformance[]
}

export const useWorkouts = () => {
  const api = useApi()

  /**
   * Fetch workout history for the current user
   * @param limit - Number of workouts to fetch (default: 10)
   * @param offset - Pagination offset (default: 0)
   */
  const fetchHistory = async (
    limit: number = 10,
    offset: number = 0
  ): Promise<WorkoutSession[]> => {
    return await api.get<WorkoutSession[]>(
      `/api/v1/workouts/history?limit=${limit}&offset=${offset}`
    )
  }

  /**
   * Fetch details of a specific workout session
   * @param sessionId - Workout session ID
   */
  const fetchWorkout = async (sessionId: string): Promise<WorkoutSession> => {
    return await api.get<WorkoutSession>(`/api/v1/workouts/${sessionId}`)
  }

  /**
   * Save a completed workout to the database
   * Backend calculates calories and checks for achievements
   * @param workoutData - Completed workout session data
   */
  const saveWorkout = async (
    workoutData: WorkoutSessionCreate
  ): Promise<WorkoutSession> => {
    return await api.post<WorkoutSession>('/api/v1/workouts', workoutData)
  }

  return {
    fetchHistory,
    fetchWorkout,
    saveWorkout,
  }
}
