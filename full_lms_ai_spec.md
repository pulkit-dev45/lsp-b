# Full LMS Specification & Prompt for AI (Django + HTMX + Tailwind)

## 🎯 Goal
You are an expert UI/UX developer specializing in minimalist, world-class design systems. Your task is to generate the entire HTML/CSS frontend templates for a complete Learning Management System (LMS) built with Django, styled strictly according to **Steve Jobs' Design Philosophy** (Apple typography, hyper-clean white aesthetic, precise spacing, zero unnecessary clutter, high contrast, and tactile micro-interactions).

---

## 🛑 Design System & Guidelines

### 1. Aesthetic Guidelines (Steve Jobs / Minimalist Apple Style)
* **Color Palette:**
  * **Primary Background:** Absolute clean white (`#FFFFFF`) or subtle off-white canvas (`#FAFAFA`).
  * **Text:** Deep charcoal black (`#000000` or `#111111`) for maximum readability. Secondary text in desaturated grey (`#666666`).
  * **Accents:** Muted neutral darks or subtle system blue (`#0066CC`) used *sparingly* only for actionable focal points.
* **Typography:**
  * Clean, humanistic sans-serif font stack: `-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif`.
  * Generous line heights (`leading-relaxed`), strong contrast between large titles (`text-3xl` to `text-5xl`, `font-semibold`) and clean body text (`text-base`).
* **Borders & Shadows:**
  * Crisp, razor-thin borders (`border border-neutral-200/80` or `border-neutral-100`).
  * Subtle elevation using soft, ambient drop shadows (`shadow-sm` or `shadow-md` with low opacity). Avoid heavy, harsh dark shadows.
* **Layout & Whitespace:**
  * **Extreme Whitespace:** Give elements plenty of breathing room. Large padding (`p-6`, `p-8`, `py-12`).
  * Maximum content container width: `max-w-6xl` or `max-w-7xl` centered with `mx-auto`.

---

## 🛠️ Tech Stack Constraints
* **Backend Integration:** Django Templates (`DTL`)
* **Styling:** Tailwind CSS (via CDN or standard build)
* **Interactivity:** HTMX (Strictly no heavy React/Vue JS frameworks!)
* **Icons:** Lucide-Icons or clean inline SVGs

---

## 🗄️ Expected Django Models Structure

The generated templates must map cleanly to these Django models:

* **CustomUser:** Profile picture, bio, headline, social links.
* **Course:** Title, slug, description, thumbnail, instructor, price.
* **Module:** Course FK, title, order.
* **Lesson:** Module FK, title, content, video_url, duration, order.
* **Enrollment:** User FK, Course FK, enrolled_at, progress_percentage.
* **LessonProgress:** User FK, Lesson FK, is_completed, completed_at.
* **Certificate:** User FK, Course FK, issued_at, verification_id.

---

## 📦 Complete Template Suite to Generate

### 1. Global Base Layout (`templates/base.html`)
* HTML5 template with meta tags, Tailwind CDN, and HTMX scripts.
* Glassmorphism header navbar with links (Courses, Dashboard, Profile, Certificates, Auth buttons).
* Toast notification container for HTMX messages.
* Clean footer with links and copyright notice.

### 2. Course Catalog & Landing (`templates/courses/course_list.html`)
* Hero banner with search bar driving dynamic HTMX filtering (`hx-get="{% url 'course-search' %}"`).
* Course grid featuring course cards with progress badges, category tags, and duration.

### 3. Student Dashboard (`templates/dashboard/index.html`)
* Header with greeting and top-level stats (In Progress, Completed, Earned Certificates).
* Enrolled courses grid with dynamic progress bars and a "Continue Learning →" shortcut.
* Tabs powered by HTMX (`#dashboard-content`) for switching between Enrolled, Saved, and Completed courses.

### 4. Course Detail & Enrollment (`templates/courses/course_detail.html`)
* Two-column split layout:
  * **Left:** Course overview, instructor details, expandable module accordion.
  * **Right Sticky Card:** Enrollment button (swaps to "Go to Course" if enrolled via HTMX), duration, level, prerequisites.

### 5. Lesson Player Workspace (`templates/courses/lesson_detail.html`)
* **Left Sidebar (Collapsible):** Module tree listing chapters and lessons with checkmarks for completed ones.
* **Main Area:** Video container / markdown reader, resource download attachments, and Next/Previous navigation.
* **HTMX Toggle Action:** "Mark as Complete" button that asynchronously checks off the lesson and updates the progress bar without page reload.

### 6. User Profile & Settings (`templates/accounts/profile.html`)
* Profile avatar, headline, bio, and enrolled course history.
* Settings tabs (HTMX powered): Update Personal Info, Password Change, and Public Profile settings.

### 7. Certificate & Public Verification (`templates/certificates/detail.html`)
* Printable, elegant certificate frame with completion date, instructor signature block, and unique verification ID hash.
* "Download PDF" button and public verification status badge.

### 8. HTMX Partials (`templates/courses/partials/`)
* `course_cards.html`: Course list fragment for dynamic search updates.
* `lesson_progress.html`: Dynamic sidebar checkmark fragment.
* `enroll_button.html`: Dynamic enrollment CTA state swap.

---

## ⚡ Instructions for the Frontend AI
1. Do not use React, Vue, or any client-side JavaScript framework.
2. Rely entirely on standard HTML5, Tailwind CSS, and HTMX attributes (`hx-get`, `hx-post`, `hx-target`, `hx-swap`).
3. Maintain extreme whitespace, clean typography, thin borders, and an overall Apple-esque aesthetic.
