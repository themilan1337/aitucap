/**
 * Achievements Composable
 * Handles fetching user achievements and badges
 */

export interface Achievement {
  id: string
  user_id: string
  achievement_type: string
  name: string
  description: string
  icon: string
  unlocked_at?: string
  progress: number
  target: number
  created_at: string
}

export const useAchievements = () => {
  const api = useApi()

  /**
   * Fetch all achievements for the current user
   * Includes both unlocked and locked achievements
   */
  const fetchAchievements = async (): Promise<Achievement[]> => {
    return await api.get<Achievement[]>('/api/v1/achievements')
  }

  /**
   * Fetch only unlocked achievements
   */
  const fetchUnlockedAchievements = async (): Promise<Achievement[]> => {
    const achievements = await fetchAchievements()
    return achievements.filter(a => a.unlocked_at !== null)
  }

  /**
   * Fetch achievement progress (locked achievements)
   */
  const fetchLockedAchievements = async (): Promise<Achievement[]> => {
    const achievements = await fetchAchievements()
    return achievements.filter(a => a.unlocked_at === null)
  }

  return {
    fetchAchievements,
    fetchUnlockedAchievements,
    fetchLockedAchievements,
  }
}
