/**
 * Plan Management Composable
 * Handles fetching and generating 30-day workout plans
 */

export interface PlanDay {
  id: string
  day_number: number
  date: string
  is_rest_day: boolean
  is_completed: boolean
  completed_at?: string
  exercises: PlannedExercise[]
}

export interface PlannedExercise {
  id: string
  exercise_type: string
  target_sets: number
  target_reps: number
  estimated_minutes: number
  order_index: number
}

export interface WorkoutPlan {
  id: string
  user_id: string
  week_start_date: string
  is_active: boolean
  created_at: string
  days: PlanDay[]
}

export interface GeneratePlanResponse {
  status: string
  plan_id: string
  duration_days: number
}

export const usePlan = () => {
  const api = useApi()

  /**
   * Fetch the active workout plan for the current user
   * Returns a 30-day plan with all exercises
   */
  const fetchActivePlan = async (): Promise<WorkoutPlan> => {
    return await api.get<WorkoutPlan>('/api/v1/plans/current')
  }

  /**
   * Generate a new 30-day workout plan
   * Deactivates old plans and creates a new one based on user profile
   */
  const generatePlan = async (): Promise<GeneratePlanResponse> => {
    return await api.post<GeneratePlanResponse>('/api/v1/plans/generate')
  }

  return {
    fetchActivePlan,
    generatePlan,
  }
}
