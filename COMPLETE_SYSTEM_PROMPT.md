# 🎯 Complete MuscleUp Vision Web Dashboard - Implementation Prompt

## 📋 PROJECT CONTEXT

You are working on **MuscleUp Vision**, an AI-powered fitness tracking web application that uses computer vision (RTMPose) to track exercises in real-time via webcam. The backend (FastAPI + PostgreSQL + Redis) and frontend (Nuxt 3) are ~60% complete. Your task is to **finish the remaining 40%** to make the application fully functional.

### Current State
- ✅ Backend API with all endpoints working
- ✅ Computer vision (RTMPose) WebSocket fully functional
- ✅ AI workout plan generation (Azure OpenAI) working
- ✅ Beautiful UI components built in Nuxt 3
- ❌ Dashboard NOT connected to backend APIs (uses mock data)
- ❌ Workout sessions NOT saved to database after training
- ❌ Missing business logic (calories, achievements, form corrections)

---

## 🎯 YOUR MISSION: Complete These 6 Critical Tasks

### **TASK 1: Connect Plan Page to Real API**
**File**: `dashboard/app/pages/plan.vue`

**Current Problem**: Shows hardcoded mock exercises and calendar

**What to Implement**:
1. Fetch active plan from `GET /api/v1/plans/active`
2. Display real plan days in calendar strip with correct dates
3. Show today's exercises from the plan
4. Mark completed days with checkmark
5. Add "Regenerate Plan" button that calls `POST /api/v1/plans/generate`
6. Handle loading states and errors
7. Pass correct exercises to training page when "Start" is clicked

**API Response Format**:
```typescript
interface Plan {
  id: string
  user_id: string
  created_at: string
  is_active: boolean
  plan_days: PlanDay[]
}

interface PlanDay {
  id: string
  day_number: number
  target_muscle_group: string
  is_rest_day: boolean
  is_completed: boolean
  completed_at: string | null
  exercises: Exercise[]
}

interface Exercise {
  exercise_type: string
  name_ru: string
  name_en: string
  sets: number
  reps: number
  duration: number | null
  rest_time: number
  order_index: number
}
```

**Implementation Checklist**:
- [ ] Create composable `usePlan()` in `dashboard/app/composables/usePlan.ts`
- [ ] Add API call with error handling
- [ ] Map plan_days to calendar view
- [ ] Calculate which day is "today" based on plan creation date
- [ ] Show loading skeleton while fetching
- [ ] Show error message if plan fetch fails
- [ ] Implement "Regenerate Plan" with confirmation dialog
- [ ] Navigate to `/train` with today's exercises

---

### **TASK 2: Connect Home Page to Real APIs**
**File**: `dashboard/app/pages/home.vue`

**Current Problem**: Stats work, but workouts history and achievements use mock data

**What to Implement**:
1. Fetch recent workouts from `GET /api/v1/workouts/history?limit=5`
2. Fetch achievements from `GET /api/v1/achievements`
3. Calculate streak from workout history
4. Make achievement badges clickable
5. Add "View All" buttons that navigate to detail pages

**API Response Formats**:
```typescript
interface WorkoutSession {
  id: string
  started_at: string
  completed_at: string
  total_duration: number
  total_calories: number
  average_form_accuracy: number
  exercises: ExercisePerformance[]
}

interface ExercisePerformance {
  exercise_type: string
  reps: number
  duration: number
  form_accuracy: number
  calories_burned: number
}

interface Achievement {
  id: string
  achievement_type: string
  name: string
  description: string
  icon: string
  progress: number
  target: number
  unlocked_at: string | null
}
```

**Implementation Checklist**:
- [ ] Create `useWorkouts()` composable
- [ ] Create `useAchievements()` composable
- [ ] Fetch workouts history and display in WorkoutHistoryCard
- [ ] Fetch achievements and update AchievementCard
- [ ] Calculate streak (consecutive days with workouts)
- [ ] Add navigation to workout details
- [ ] Show confetti when new achievement unlocked
- [ ] Handle empty states (no workouts yet, no achievements)

---

### **TASK 3: Save Workouts to Database After Training**
**File**: `dashboard/app/components/workout/WorkoutCamera.vue`

**Current Problem**: Training session completes but data is NEVER saved to database

**What to Implement**:
1. Track per-exercise statistics during workout (not just total)
2. After workout completes, POST session data to `/api/v1/workouts`
3. Show success message or confetti
4. Navigate back to home page
5. Handle save errors gracefully

**Critical Changes Needed**:

```typescript
// Add these refs to track per-exercise data
const exerciseStats = ref<Map<number, {
  reps: number
  duration: number
  formAccuracySum: number
  formAccuracyCount: number
}>>(new Map())

// Update handleRepDetected to track per-exercise
const handleRepDetected = (reps: number) => {
  const exIndex = currentExerciseIndex.value
  if (!exerciseStats.value.has(exIndex)) {
    exerciseStats.value.set(exIndex, {
      reps: 0,
      duration: 0,
      formAccuracySum: 0,
      formAccuracyCount: 0
    })
  }

  const stats = exerciseStats.value.get(exIndex)!
  stats.reps++
  stats.formAccuracySum += formQuality.value
  stats.formAccuracyCount++

  // ... rest of existing logic
}

// Update completeWorkout to save to database
const completeWorkout = async () => {
  endTime.value = new Date()
  showingResults.value = true

  // Stop camera and WebSocket
  if (frameInterval) clearInterval(frameInterval)
  if (stream.value) stream.value.getTracks().forEach(track => track.stop())
  if (ws.value) ws.value.close()

  // Prepare workout data
  const workoutData = {
    plan_day_id: null, // TODO: Get from plan in TASK 1
    started_at: startTime.value!.toISOString(),
    completed_at: endTime.value.toISOString(),
    total_duration: Math.floor((endTime.value.getTime() - startTime.value!.getTime()) / 1000),
    total_calories: Math.floor(totalReps.value * 0.5), // Will be calculated by backend
    average_form_accuracy: accuracy.value,
    exercises: props.exercises.map((ex, idx) => {
      const stats = exerciseStats.value.get(idx) || { reps: 0, duration: 0, formAccuracySum: 0, formAccuracyCount: 0 }
      return {
        exercise_type: getExerciseType(ex.name),
        reps: stats.reps,
        duration: stats.duration,
        form_accuracy: stats.formAccuracyCount > 0 ? Math.floor(stats.formAccuracySum / stats.formAccuracyCount) : 0,
        form_corrections: [],
        calories_burned: 0, // Backend will calculate
        order_index: idx
      }
    })
  }

  // Save to database
  try {
    const response = await $fetch('/api/v1/workouts', {
      method: 'POST',
      body: workoutData,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    console.log('Workout saved:', response)

    // TODO: Check for new achievements

    // Show success and navigate after delay
    setTimeout(() => {
      navigateTo('/home')
    }, 3000)

  } catch (error) {
    console.error('Failed to save workout:', error)
    // Show error but still allow user to exit
    alert('Не удалось сохранить тренировку. Попробуйте еще раз.')
  }
}
```

**Implementation Checklist**:
- [ ] Add per-exercise tracking (reps, duration, form accuracy)
- [ ] Track exercise start/end times
- [ ] Implement `saveWorkout()` function with POST to `/api/v1/workouts`
- [ ] Handle API errors gracefully
- [ ] Show success animation after save
- [ ] Navigate to home after successful save
- [ ] Update results screen to show "Saving..."
- [ ] Get `plan_day_id` from navigation state (passed from plan page)

---

### **TASK 4: Implement Calories Calculation Service**
**Files**: Create `backend/app/services/calories_service.py`

**Current Problem**: Calories fields exist but are always 0

**What to Implement**:

```python
"""
Calories calculation service using MET (Metabolic Equivalent of Task) values.
Formula: Calories = MET × Weight(kg) × Time(hours)
"""
from typing import Dict

# MET values for each exercise (Metabolic Equivalent of Task)
# Source: Compendium of Physical Activities
EXERCISE_MET_VALUES: Dict[str, float] = {
    "squat": 5.0,           # Body-weight squats
    "lunge": 4.5,           # Walking lunges
    "pushup": 8.0,          # Push-ups (vigorous)
    "plank": 4.0,           # Planks
    "situp": 8.0,           # Sit-ups (vigorous)
    "crunch": 3.8,          # Crunches
    "bicep_curl": 3.5,      # Bicep curls with body resistance
    "lateral_raise": 3.0,   # Arm raises
    "overhead_press": 4.0,  # Overhead press
    "leg_raise": 5.0,       # Leg raises
    "knee_raise": 4.0,      # Knee raises
    "knee_press": 4.0,      # Knee press
}

def calculate_exercise_calories(
    exercise_type: str,
    duration_seconds: int,
    user_weight_kg: float,
    reps: int = 0
) -> float:
    """
    Calculate calories burned for a single exercise.

    Args:
        exercise_type: Exercise identifier (e.g., "squat")
        duration_seconds: Duration of exercise in seconds
        user_weight_kg: User's weight in kilograms
        reps: Number of reps performed (optional, for additional accuracy)

    Returns:
        Calories burned (float)
    """
    met = EXERCISE_MET_VALUES.get(exercise_type, 4.0)  # Default to 4.0 if unknown
    duration_hours = duration_seconds / 3600.0

    # Base calculation
    calories = met * user_weight_kg * duration_hours

    # Bonus: Add small amount per rep for explosiveness
    rep_bonus = reps * 0.05 * user_weight_kg / 100

    return round(calories + rep_bonus, 2)

def calculate_workout_calories(
    exercises: list,
    user_weight_kg: float
) -> float:
    """
    Calculate total calories for entire workout session.

    Args:
        exercises: List of ExercisePerformance objects with exercise_type, duration, reps
        user_weight_kg: User's weight in kilograms

    Returns:
        Total calories burned
    """
    total = 0.0
    for exercise in exercises:
        calories = calculate_exercise_calories(
            exercise_type=exercise.exercise_type,
            duration_seconds=exercise.duration,
            user_weight_kg=user_weight_kg,
            reps=exercise.reps
        )
        exercise.calories_burned = calories
        total += calories

    return round(total, 2)
```

**Then Update**: `backend/app/api/v1/workouts.py`

```python
# Add at top
from app.services.calories_service import calculate_workout_calories

# In log_workout_session function, after line 21:
@router.post("/", response_model=WorkoutSessionResponse, status_code=status.HTTP_201_CREATED)
async def log_workout_session(
    workout_data: WorkoutSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Log a completed workout session with exercise details"""

    # Get user's weight for calorie calculation
    user_weight_kg = current_user.profile.weight if current_user.profile else 70.0  # Default 70kg

    # Calculate calories for each exercise and total
    exercises_list = list(workout_data.exercises)
    total_calories = calculate_workout_calories(exercises_list, user_weight_kg)

    # Create session with calculated calories
    new_session = WorkoutSession(
        user_id=current_user.id,
        plan_day_id=workout_data.plan_day_id,
        started_at=workout_data.started_at,
        completed_at=workout_data.completed_at,
        total_duration=workout_data.total_duration,
        total_calories=total_calories,  # Use calculated value
        average_form_accuracy=workout_data.average_form_accuracy
    )

    # ... rest of existing code
```

**Implementation Checklist**:
- [ ] Create `backend/app/services/calories_service.py` with functions above
- [ ] Update `backend/app/api/v1/workouts.py` to use calories service
- [ ] Test with different exercises and user weights
- [ ] Ensure calories show correctly in frontend

---

### **TASK 5: Implement Achievement Detection Service**
**Files**: Create `backend/app/services/achievement_service.py`

**Current Problem**: Achievements exist in DB but are never unlocked

**What to Implement**:

```python
"""
Achievement detection and awarding service.
Checks for milestone completions and unlocks badges.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from datetime import datetime, timedelta
from app.models.achievement import UserAchievement
from app.models.workout import WorkoutSession
from app.models.user import User
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Achievement definitions
ACHIEVEMENTS = {
    "first_workout": {
        "name": "Первая тренировка",
        "description": "Выполните первую тренировку",
        "icon": "trophy",
        "check": lambda stats: stats["total_workouts"] >= 1
    },
    "workouts_10": {
        "name": "10 тренировок",
        "description": "Выполните 10 тренировок",
        "icon": "fire",
        "check": lambda stats: stats["total_workouts"] >= 10
    },
    "workouts_50": {
        "name": "50 тренировок",
        "description": "Выполните 50 тренировок",
        "icon": "star",
        "check": lambda stats: stats["total_workouts"] >= 50
    },
    "streak_7": {
        "name": "7-дневная серия",
        "description": "Тренируйтесь 7 дней подряд",
        "icon": "flame",
        "check": lambda stats: stats["current_streak"] >= 7
    },
    "perfect_form": {
        "name": "Идеальная форма",
        "description": "Достигните 95%+ точности",
        "icon": "medal",
        "check": lambda stats: stats["best_accuracy"] >= 95
    },
    "early_bird": {
        "name": "Ранняя пташка",
        "description": "Тренируйтесь до 8 утра",
        "icon": "sunrise",
        "check": lambda stats: stats["has_morning_workout"]
    }
}

async def calculate_user_stats(user_id: str, db: AsyncSession) -> Dict:
    """Calculate statistics needed for achievement checking"""

    # Total workouts
    result = await db.execute(
        select(func.count(WorkoutSession.id))
        .filter(WorkoutSession.user_id == user_id)
    )
    total_workouts = result.scalar() or 0

    # Best accuracy
    result = await db.execute(
        select(func.max(WorkoutSession.average_form_accuracy))
        .filter(WorkoutSession.user_id == user_id)
    )
    best_accuracy = result.scalar() or 0

    # Current streak
    current_streak = await calculate_streak(user_id, db)

    # Check for morning workout
    result = await db.execute(
        select(WorkoutSession)
        .filter(
            WorkoutSession.user_id == user_id,
            func.extract('hour', WorkoutSession.started_at) < 8
        )
        .limit(1)
    )
    has_morning_workout = result.scalars().first() is not None

    return {
        "total_workouts": total_workouts,
        "current_streak": current_streak,
        "best_accuracy": best_accuracy,
        "has_morning_workout": has_morning_workout
    }

async def calculate_streak(user_id: str, db: AsyncSession) -> int:
    """Calculate current workout streak (consecutive days)"""

    # Get all workout dates (distinct days)
    result = await db.execute(
        select(func.date(WorkoutSession.completed_at).label('workout_date'))
        .filter(WorkoutSession.user_id == user_id)
        .distinct()
        .order_by(desc('workout_date'))
    )
    workout_dates = [row[0] for row in result.all()]

    if not workout_dates:
        return 0

    # Check if most recent workout was today or yesterday
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    if workout_dates[0] not in [today, yesterday]:
        return 0  # Streak broken

    # Count consecutive days
    streak = 1
    expected_date = workout_dates[0] - timedelta(days=1)

    for workout_date in workout_dates[1:]:
        if workout_date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break

    return streak

async def check_and_award_achievements(
    user_id: str,
    db: AsyncSession
) -> List[Dict]:
    """
    Check for new achievements and award them.
    Returns list of newly unlocked achievements.
    """

    # Calculate user stats
    stats = await calculate_user_stats(user_id, db)

    # Get already unlocked achievements
    result = await db.execute(
        select(UserAchievement.achievement_type)
        .filter(
            UserAchievement.user_id == user_id,
            UserAchievement.unlocked_at.isnot(None)
        )
    )
    unlocked_types = {row[0] for row in result.all()}

    # Check each achievement
    newly_unlocked = []

    for achievement_type, achievement_def in ACHIEVEMENTS.items():
        # Skip if already unlocked
        if achievement_type in unlocked_types:
            continue

        # Check if condition is met
        if achievement_def["check"](stats):
            # Award achievement
            new_achievement = UserAchievement(
                user_id=user_id,
                achievement_type=achievement_type,
                name=achievement_def["name"],
                description=achievement_def["description"],
                icon=achievement_def["icon"],
                unlocked_at=datetime.utcnow(),
                progress=100,
                target=100
            )
            db.add(new_achievement)

            newly_unlocked.append({
                "type": achievement_type,
                "name": achievement_def["name"],
                "description": achievement_def["description"],
                "icon": achievement_def["icon"]
            })

            logger.info(f"Achievement unlocked: {achievement_type} for user {user_id}")

    if newly_unlocked:
        await db.commit()

    return newly_unlocked
```

**Then Update**: `backend/app/api/v1/workouts.py`

```python
# Add import
from app.services.achievement_service import check_and_award_achievements

# At the end of log_workout_session, before return:
    await db.commit()
    await db.refresh(new_session)

    # Check for new achievements
    newly_unlocked = await check_and_award_achievements(current_user.id, db)
    if newly_unlocked:
        logger.info(f"New achievements unlocked: {newly_unlocked}")

    # Explicitly load exercises for the response
    result = await db.execute(
        select(ExercisePerformance)
        .filter(ExercisePerformance.workout_session_id == new_session.id)
        .order_by(ExercisePerformance.order_index)
    )
    new_session.exercises = result.scalars().all()

    # Attach newly unlocked achievements to response (optional)
    # You can add this to the response model if needed

    return new_session
```

**Implementation Checklist**:
- [ ] Create `backend/app/services/achievement_service.py`
- [ ] Implement streak calculation logic
- [ ] Implement achievement checking logic
- [ ] Update workouts endpoint to check achievements after save
- [ ] Test each achievement unlocks correctly
- [ ] Show confetti in frontend when achievement unlocked

---

### **TASK 6: Add Form Correction Suggestions**
**File**: `backend/app/workouts/exercise_counter.py`

**Current Problem**: `form_corrections` is always an empty array

**What to Implement**:
Add logic to detect form issues and generate correction messages.

**Find this class and update**:

```python
class ExerciseCounter:
    def __init__(self, exercises_config: Dict[str, Any]):
        self.exercises_config = exercises_config
        self.counter = 0
        self.stage = None
        self.last_angle = None
        self.form_corrections = []  # Add this

    def get_form_corrections(self) -> List[str]:
        """Return accumulated form corrections for the current rep"""
        corrections = self.form_corrections.copy()
        self.form_corrections = []  # Reset after getting
        return corrections

    def count(self, angle: float, exercise_type: str) -> int:
        """
        Count repetitions based on angle changes.
        Also detect form issues.
        """
        if angle is None:
            return self.counter

        exercise_config = self.exercises_config.get("exercises", {}).get(exercise_type)
        if not exercise_config:
            return self.counter

        up_threshold = exercise_config.get("up_threshold", 160)
        down_threshold = exercise_config.get("down_threshold", 90)
        ideal_down_angle = exercise_config.get("ideal_down_angle", 90)
        ideal_up_angle = exercise_config.get("ideal_up_angle", 170)

        # Detect form issues
        self._check_form_quality(angle, exercise_type, ideal_down_angle, ideal_up_angle, down_threshold, up_threshold)

        # Count reps (existing logic)
        if angle > up_threshold:
            if self.stage == 'down':
                self.counter += 1
                self.stage = 'up'
        elif angle < down_threshold:
            self.stage = 'down'

        self.last_angle = angle
        return self.counter

    def _check_form_quality(
        self,
        angle: float,
        exercise_type: str,
        ideal_down: float,
        ideal_up: float,
        down_threshold: float,
        up_threshold: float
    ):
        """Analyze form and add corrections if needed"""

        # Squat-specific corrections
        if exercise_type == "squat":
            if self.stage == 'down' and angle > down_threshold + 20:
                self.form_corrections.append("Присядьте глубже - колени должны быть под углом 90°")
            elif self.stage == 'up' and angle < up_threshold - 10:
                self.form_corrections.append("Полностью выпрямите ноги")

        # Pushup-specific corrections
        elif exercise_type == "pushup":
            if self.stage == 'down' and angle > down_threshold + 15:
                self.form_corrections.append("Опуститесь ниже - грудь ближе к полу")
            elif self.stage == 'up' and angle < up_threshold - 15:
                self.form_corrections.append("Полностью выпрямите руки")

        # Lunge-specific corrections
        elif exercise_type == "lunge":
            if self.stage == 'down' and angle > down_threshold + 20:
                self.form_corrections.append("Опустите колено ниже - угол 90°")

        # General correction for not reaching full range
        if self.last_angle is not None:
            angle_change = abs(angle - self.last_angle)
            if angle_change < 5 and self.stage is not None:
                self.form_corrections.append("Увеличьте амплитуду движения")
```

**Then update response in** `backend/app/api/v1/vision.py`:

```python
# Around line 148, update response to include form corrections:
response: Dict[str, Any] = {
    "success": True,
    "exercise": exercise_type,
    "reps": proc.exercise_counter.get_counter(),
    "stage": proc.exercise_counter.get_stage(),
    "form_corrections": proc.exercise_counter.get_form_corrections()  # Add this
}
```

**Then in frontend** `dashboard/app/components/workout/WorkoutCamera.vue`:

```typescript
// Add state for corrections
const formCorrections = ref<string[]>([])

// In WebSocket onmessage handler, add:
if (data.form_corrections && data.form_corrections.length > 0) {
  formCorrections.value = data.form_corrections

  // Auto-hide after 3 seconds
  setTimeout(() => {
    formCorrections.value = []
  }, 3000)
}

// In template, add correction display (around line 634):
<!-- Form Corrections Display -->
<div v-if="formCorrections.length > 0" class="absolute top-32 left-0 right-0 px-6">
  <div class="bg-orange-500/90 backdrop-blur rounded-xl p-4 text-white">
    <div class="flex items-start gap-2">
      <Icon icon="heroicons:exclamation-triangle" class="text-xl flex-shrink-0 mt-0.5" />
      <div class="flex-1">
        <p class="font-bold text-sm mb-1">Улучшите технику:</p>
        <ul class="text-sm space-y-1">
          <li v-for="(correction, idx) in formCorrections" :key="idx">
            {{ correction }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>
```

**Implementation Checklist**:
- [ ] Update `ExerciseCounter` class with form checking logic
- [ ] Add corrections for squat, pushup, lunge, plank
- [ ] Update vision WebSocket to send corrections
- [ ] Display corrections in WorkoutCamera UI
- [ ] Test corrections appear during workout
- [ ] Save corrections to ExercisePerformance records

---

## 🎨 BONUS TASKS (Polish & UX)

### **BONUS 1: Add Loading States**
Add loading spinners/skeletons to:
- Plan page while fetching plan
- Home page while fetching stats/workouts/achievements
- During workout save operation

```vue
<!-- Example skeleton -->
<div v-if="loading" class="space-y-4">
  <div class="bg-[#111] rounded-2xl p-5 animate-pulse">
    <div class="h-4 bg-white/10 rounded w-1/4 mb-4"></div>
    <div class="h-8 bg-white/10 rounded w-3/4"></div>
  </div>
</div>
```

### **BONUS 2: Add Error Handling**
Wrap all API calls in try-catch with user-friendly messages:

```typescript
try {
  const plan = await $fetch('/api/v1/plans/active')
  // ...
} catch (error) {
  console.error('Failed to fetch plan:', error)
  showToast('Не удалось загрузить план. Попробуйте обновить страницу.', 'error')
}
```

### **BONUS 3: Add Empty States**
Show friendly messages when no data exists:
- "У вас пока нет активного плана. Создайте свой первый план!"
- "У вас пока нет завершенных тренировок. Начните первую тренировку!"

### **BONUS 4: Improve Progress Page**
- Fetch data from `/api/v1/stats/weekly` with date range selector
- Add personal records section
- Add exercise-specific breakdowns

---

## 📦 IMPLEMENTATION ORDER

**Follow this exact order to avoid dependencies:**

1. **TASK 4** - Calories Service (backend, no dependencies)
2. **TASK 5** - Achievement Service (backend, no dependencies)
3. **TASK 6** - Form Corrections (backend + frontend)
4. **TASK 1** - Plan Page (frontend, depends on backend being stable)
5. **TASK 2** - Home Page (frontend, depends on achievements service)
6. **TASK 3** - Workout Persistence (frontend, depends on all backend services)
7. **BONUS TASKS** - Polish (add after core features work)

---

## ✅ TESTING CHECKLIST

After implementing all tasks, test this complete user journey:

1. [ ] **Signup Flow**
   - Login with Google
   - Complete onboarding (profile, goals, fitness level)
   - Verify profile saved

2. [ ] **Plan Generation**
   - Go to Plan page
   - Verify plan is auto-generated (if first time)
   - Verify plan shows correct exercises
   - Verify calendar shows 7 days
   - Verify "today" is highlighted

3. [ ] **Workout Flow**
   - Click "Start" on Plan page
   - Verify camera opens
   - Verify WebSocket connects
   - Verify skeleton overlay appears
   - Perform 3-5 reps of exercise
   - Verify rep counter increments
   - Verify form corrections appear (intentionally do bad form)
   - Complete first set
   - Verify rest timer appears
   - Complete entire workout
   - Verify results screen shows stats
   - Verify workout saves to database
   - Verify navigation back to home

4. [ ] **Post-Workout**
   - Verify home page shows new workout in history
   - Verify stats updated (total workouts increased)
   - Verify achievement unlocked (e.g., "First Workout")
   - Verify confetti appears
   - Verify plan page marks day as completed

5. [ ] **Progress Tracking**
   - Go to Progress page
   - Verify charts show real data
   - Verify accuracy trend updates
   - Verify workout frequency shows

6. [ ] **Multi-Day Test**
   - Do workout on 3 consecutive days
   - Verify streak increases
   - Verify "7-day streak" achievement tracked

---

## 🚨 CRITICAL NOTES

1. **Use `credentials: 'include'`** in all $fetch calls (for HttpOnly cookies)
2. **Use `try-catch`** around ALL API calls
3. **Test with real camera** - don't just mock the data
4. **Test calorie calculation** with different user weights
5. **Test achievement unlocking** by manually inserting workout records
6. **Verify CORS headers** allow credentials (already configured in backend)
7. **Check browser console** for WebSocket errors
8. **Test mobile responsive** - camera should work on mobile

---

## 📂 FILES YOU'LL MODIFY/CREATE

### Backend (Python)
- ✅ `backend/app/services/calories_service.py` (CREATE)
- ✅ `backend/app/services/achievement_service.py` (CREATE)
- ✅ `backend/app/api/v1/workouts.py` (MODIFY)
- ✅ `backend/app/workouts/exercise_counter.py` (MODIFY)
- ✅ `backend/app/api/v1/vision.py` (MODIFY)

### Frontend (Vue/TypeScript)
- ✅ `dashboard/app/pages/plan.vue` (MODIFY)
- ✅ `dashboard/app/pages/home.vue` (MODIFY)
- ✅ `dashboard/app/components/workout/WorkoutCamera.vue` (MODIFY)
- ✅ `dashboard/app/composables/usePlan.ts` (CREATE)
- ✅ `dashboard/app/composables/useWorkouts.ts` (CREATE)
- ✅ `dashboard/app/composables/useAchievements.ts` (CREATE)

---

## 🎯 SUCCESS CRITERIA

**The system is complete when:**
- ✅ User can complete full journey from signup to workout to seeing results
- ✅ All data persists to database
- ✅ Achievements unlock automatically
- ✅ Calories calculate correctly
- ✅ Form corrections appear during workout
- ✅ Plan page shows real plan data
- ✅ Home page shows real workout history
- ✅ Progress page shows real analytics
- ✅ No console errors
- ✅ No 404/500 API errors
- ✅ Works on desktop and mobile browsers

---

## 🚀 START CODING NOW!

Begin with **TASK 4** (Calories Service) and work through each task in order. Test thoroughly after each task. Good luck! 🎉
