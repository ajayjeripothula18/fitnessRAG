# FitnessRAG — User Flows
## Created by Zara (Senior UX/Frontend Engineer)
## Last Updated: 2026-08-31

---

## 1. Onboarding Flow (New User)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Landing /   │     │  Sign Up     │     │  Profile     │     │  Dashboard   │
│  Login Page  │────▶│  Form        │────▶│  Completion  │────▶│  (First Use) │
│              │     │              │     │  Wizard      │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                            │                    │
                     ┌──────┴──────┐      ┌──────┴──────┐
                     │ Validation  │      │  4 Steps:   │
                     │ Errors      │      │  1. Basic   │
                     │ (inline)    │      │  2. Goals   │
                     └─────────────┘      │  3. Equip   │
                                          │  4. Diet    │
                                          └─────────────┘
```

### Step-by-Step

1. **Landing Page**
   - User sees app overview, key features, and CTA buttons
   - Options: "Sign Up" or "Log In"
   - Google OAuth button available

2. **Sign Up Form**
   - Fields: Full name, Email, Password, Confirm Password
   - Real-time inline validation
   - Password strength indicator
   - On success → Email verification sent → Profile Wizard

3. **Profile Completion Wizard** (4 steps, can skip but encouraged)
   - **Step 1 — Basic Info**: Age range, Sex, Height, Weight
   - **Step 2 — Fitness Goals**: Primary goal (dropdown), Fitness level
   - **Step 3 — Equipment**: Multi-select of available equipment
   - **Step 4 — Dietary Preferences**: Diet type, Allergies
   - Progress bar shows completion (each step = 25%)
   - "Skip for now" option on each step

4. **Dashboard (First Use)**
   - Welcome message with user's name
   - Quick action cards: "Start a Conversation", "Create a Plan", "Log a Measurement"
   - Profile completion prompt if < 100%
   - Empty states for plans and tracking (encouraging copy)

---

## 2. Login Flow (Returning User)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Login Page  │────▶│  Dashboard   │     │  Last Active │
│              │     │              │────▶│  Conversation│
│  Email +     │     │  Welcome     │     │  or Plan     │
│  Password    │     │  Back!       │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
       │
┌──────┴──────┐
│  Forgot     │
│  Password?  │──▶ Reset Flow (email → token → new password)
└─────────────┘
```

---

## 3. Conversational AI Coach Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Coach Tab   │     │  Chat        │     │  AI Response  │
│  (Bottom Nav)│────▶│  Interface   │────▶│  (Streaming) │
│              │     │              │     │              │
└──────────────┘     └──────┬───────┘     └──────┬───────┘
                            │                     │
                     ┌──────┴──────┐       ┌──────┴──────┐
                     │ History     │       │ Source      │
                     │ Sidebar     │       │ Citations   │
                     │ (threads)   │       │ (expandable)│
                     └─────────────┘       └─────────────┘
```

### Chat Interface Details

1. **Entry Point**: Bottom nav "Coach" icon → Chat screen
2. **New Conversation**: "+" button creates new thread with optional title
3. **Message Input**:
   - Text input with send button
   - Placeholder: "Ask me about workouts, nutrition, or fitness..."
   - Max 2000 chars
4. **AI Response**:
   - Typing indicator while processing
   - Streaming text appears token-by-token
   - Source citations appear as collapsible cards below response
   - Safety disclaimer banners (if medical content detected)
5. **Conversation History**:
   - Left sidebar (desktop) or drawer (mobile) shows past conversations
   - Search conversations by text
   - Delete conversation option

### Safety Flow Within Chat

```
User types message
       │
       ▼
┌──────────────────────┐
│ Safety Classification │
│ (invisible to user)   │
└──────────┬───────────┘
           │
     ┌─────┴─────┬──────────┬──────────┐
     ▼           ▼          ▼          ▼
   SAFE       MEDICAL    HARMFUL    OUT_OF_SCOPE
     │           │          │          │
     ▼           ▼          ▼          ▼
  Normal     ⚠️ Yellow   🚫 Red     🔄 Blue
  Response   Banner +    Banner +   Banner +
             Disclaimer  Blocked    Redirect
             + Education Message    Suggestion
```

---

## 4. Plan Generation Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Plans Tab   │     │  Choose:     │     │  Generation  │     │  Plan View   │
│  (Bottom Nav)│────▶│  Template or │────▶│  Loading     │────▶│  Day-by-Day  │
│              │     │  AI Generate │     │  (15-30s)    │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                            │                                         │
                     ┌──────┴──────┐                          ┌──────┴──────┐
                     │  Customize  │                          │  Actions:   │
                     │  Preferences│                          │  Edit/Save  │
                     │  (optional) │                          │  Version    │
                     └─────────────┘                          │  Archive    │
                                                              └─────────────┘
```

### Plan View (Day-by-Day)

```
┌─────────────────────────────────────────────┐
│  📋 My Push/Pull/Legs Plan          v2  📝  │
│  ─────────────────────────────────────────── │
│                                              │
│  [Mon] [Tue] [Wed] [Thu] [Fri] [Sat] [Sun]  │
│   Push  Pull  Rest  Legs  Upper Rest  Rest   │
│                                              │
│  ── Monday: Push Day ──                      │
│                                              │
│  🔥 Warm-up                                  │
│  5 min light cardio + shoulder circles       │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │ 1. Barbell Bench Press               │    │
│  │    4 × 8-10 reps | Rest: 90s        │    │
│  │    💪 Chest, Triceps, Front Delts    │    │
│  │    📝 Focus on controlled eccentric   │    │
│  │                          [Log] [Swap] │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │ 2. Overhead Dumbbell Press           │    │
│  │    3 × 10-12 reps | Rest: 60s       │    │
│  │    💪 Shoulders, Triceps             │    │
│  │                          [Log] [Swap] │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  🧘 Cool-down                                │
│  5 min chest/shoulder stretches              │
│                                              │
│  ─────────────────────────────────────────── │
│  [Start Workout]        [Modify via Chat 💬] │
└─────────────────────────────────────────────┘
```

---

## 5. Progress Tracking Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Progress    │     │  Dashboard:  │     │  Detail View │
│  Tab         │────▶│  Charts +    │────▶│  Full History│
│  (Bottom Nav)│     │  Quick Log   │     │  & Export    │
└──────────────┘     └──────┬───────┘     └──────────────┘
                            │
                     ┌──────┴──────┐
                     │  Log Entry  │
                     │  • Body     │
                     │  • Workout  │
                     └─────────────┘
```

### Progress Dashboard

```
┌─────────────────────────────────────────────┐
│  📊 Your Progress                           │
│  ─────────────────────────────────────────── │
│                                              │
│  Period: [1W] [1M] [3M] [6M] [All]          │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │  Weight Trend                        │    │
│  │  📉 ─────────────────               │    │
│  │     80.0 → 78.5 kg (-1.5)           │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │  Body Fat Estimate                   │    │
│  │  📉 ─────────────────               │    │
│  │     20.0% → 18.5% (-1.5%)           │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │  Workouts This Month: 16            │    │
│  │  ████████████████░░░░ 80% adherence  │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  ─────────────────────────────────────────── │
│  [+ Log Measurement]  [+ Log Workout]        │
└─────────────────────────────────────────────┘
```

---

## 6. Navigation Map

```
                    ┌───────────────────┐
                    │   Landing Page    │
                    │   (Unauthenticated)│
                    └────────┬──────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
            ┌──────────┐        ┌──────────┐
            │  Login   │        │  Sign Up │
            └────┬─────┘        └────┬─────┘
                 │                   │
                 └─────────┬─────────┘
                           │
                    ┌──────┴──────┐
                    │  Profile    │
                    │  Wizard     │
                    │  (if new)   │
                    └──────┬──────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │              AUTHENTICATED APP              │
    │                                              │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ ┌─────────┐
    │  │Dashboard│ │  Coach  │ │  Plans  │ │Progress│ │ Profile │
    │  │  (Home) │ │  (Chat) │ │         │ │        │ │         │
    │  └─────────┘ └─────────┘ └─────────┘ └────────┘ └─────────┘
    │       │           │           │          │           │
    │       │     ┌─────┴─────┐    │    ┌─────┴─────┐     │
    │       │     │ Thread    │    │    │ Log Body  │     │
    │       │     │ History   │    │    │ Log Work  │     │
    │       │     └───────────┘    │    │ Charts    │     │
    │       │                      │    └───────────┘     │
    │       │               ┌──────┴──────┐               │
    │       │               │ Plan Detail │               │
    │       │               │ Day View    │               │
    │       │               │ Version Hx  │               │
    │       │               └─────────────┘               │
    │                                                      │
    │  ════════════════════════════════════════════════════ │
    │  [🏠 Home] [💬 Coach] [📋 Plans] [📊 Progress] [👤 Profile] │
    └──────────────────────────────────────────────────────┘
```

---

## 7. Error & Edge Case Flows

### Network Error
- Show toast: "Connection lost. Retrying..."
- Auto-retry 3 times with exponential backoff
- After 3 failures: "Unable to connect. Check your internet and try again." + retry button

### Session Expired
- Token refresh happens silently in background
- If refresh fails: redirect to login with message "Your session has expired. Please log in again."
- Preserve last route for redirect after re-login

### AI Timeout
- Show "The AI is taking longer than usual..."
- After 15s: "Still working on it... AI responses can take up to 30s"
- After 30s: "Something went wrong. Please try again." + retry button

### Empty States
- **No conversations**: "Start your first conversation! 💬 Ask me about workouts, nutrition, or fitness goals."
- **No plans**: "You don't have any plans yet. Create one or browse templates!"
- **No measurements**: "Track your progress! Log your first measurement to see trends."

---

## 8. Responsive Breakpoints

| Device | Width | Layout Changes |
|--------|-------|----------------|
| Mobile (default) | 375-767px | Single column, bottom nav, drawer for history |
| Tablet | 768-1023px | Wider cards, side panel for chat history |
| Desktop | 1024px+ | Sidebar navigation, split view for chat, multi-column dashboard |

### Mobile-First Priority
Since this is a gym-use app, mobile is the primary experience:
- Touch-friendly targets (min 44×44px)
- Large fonts for exercise cards (readable at arm's length)
- Swipe gestures for day navigation in plans
- Bottom sheet modals instead of centered popups
