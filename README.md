 E-Learning Platform Knowledge Base

This document is a complete factual reference for the E-Learning Platform. It is intended as the corpus for the Tara AI RAG chatbot. Each section is self-contained so it can be chunked safely for vector embedding.

---

## 1. What is this platform?

The E-Learning Platform is a web-based learning management system where students enroll in courses, watch video lessons, complete topic checklists, attempt quizzes, and rate the courses they finish. It supports three user roles: **student**, **instructor**, and **admin**. The platform is free — all courses are free to enroll in, and there is no payment system.

The platform is built with React 19 + Vite on the frontend and Node.js + Express + MongoDB on the backend. Authentication uses JWT tokens after a one-time-password (OTP) email verification at signup. The built-in assistant is called **Tara**, an AI-powered chatbot trained on this knowledge base.

---

## 2. Creating an account (signup)

Signup is a two-step process that uses an email OTP:

1. On the **Signup** page, the user fills in: full name, email, password, confirm password, and role (student, instructor, or admin).
2. After clicking **Send OTP**, a 6-digit numeric code is emailed to the address. The OTP is valid for **10 minutes**.
3. The user enters the OTP and clicks **Verify OTP** to complete signup. On success they are issued a JWT token and redirected to their role-specific dashboard.

### Signup validation rules
- **Name**: required, more than 4 characters, only letters, numbers, and spaces.
- **Email**: required, must be a valid email format.
- **Password**: required, minimum 6 characters.
- **Confirm password**: must match the password exactly.
- **Role**: must be one of `student`, `instructor`, or `admin`.

Passwords are hashed with bcryptjs (10 salt rounds) before being stored. They are never stored or returned in plain text.

---

## 3. Logging in and resetting a password

### Login
The **Login** page accepts an email and password. On success the user is redirected to `/dashboard/student`, `/dashboard/instructor`, or `/dashboard/admin` depending on their role. The JWT token is stored in the browser so the user remains logged in across page reloads.

### Forgot password / password reset
The Login page exposes a **Forgot Password** link. The reset flow:
1. User enters their email and requests a reset OTP (`/api/auth/send-forgot-otp`).
2. A 6-digit OTP is sent by email, valid for 10 minutes.
3. User submits the OTP plus a new password to `/api/auth/reset-password`.
4. The new password replaces the old one. The user can then log in normally.

If the user forgets which email they registered with, they need to contact an administrator — there is no username recovery flow.

---

## 4. User roles and what each one can do

| Role | Main capabilities |
|------|--------------------|
| **Student** | Browse courses, enroll for free, watch lessons, mark topics complete, take quizzes, rate completed courses, file complaints, view own performance analytics, edit profile. |
| **Instructor** | Create and publish courses, upload materials (text or PDF), build quizzes (single-choice, multi-select, or text answer), set quiz deadlines and max attempts, view enrollment lists per course, view per-student performance analytics, view course analytics, manage own profile. |
| **Admin** | Verify unverified instructors, remove instructors (which also deletes their courses), remove student accounts, delete any course on the platform, view all complaints and resolve them with a feedback message to the student. |

Roles are chosen at signup and stored on the user account. Each role has its own dashboard.

---

## 5. Browsing and enrolling in courses

Students see all available courses on the **Browse Courses** tab of the Student Dashboard. Each course card shows the title, description, thumbnail, total duration, instructor name, and a star rating. Enrollment is one click — there is no payment, application, or approval step. Once a student clicks **Enroll**, the course immediately appears on the **Enrolled Courses** tab.

A few courses are marked **mandatory** (`isMandatory: true`). Mandatory courses are highlighted but still require the student to click enroll. Currently the mandatory courses are:
- *Programming in C: Foundational Mechanics*
- *Introduction to Python Core Syntax*
- *Java Programming Foundations*

A student cannot enroll in the same course twice — the system blocks duplicate enrollments. A student can un-enroll only by contacting an admin; there is no self-service un-enroll button.

---

## 6. Taking a course (the Course Player)

Clicking **Continue Learning** on any enrolled course opens the **Course Player**. The player shows:
- The course title and description at the top.
- A sidebar list of all topics in the course.
- A video area that embeds the YouTube video for the currently selected topic.
- A **Mark Complete** button below the video.
- Materials section (PDFs are previewed in-browser; text documents can be downloaded).
- A progress bar showing `completed topics / total topics`.

Each course currently has **5 topics**. When the student clicks **Mark Complete** on a topic, that topic name is added to their `completedTopics` list and their overall `progress` percentage is recalculated. When the percentage reaches **100%**, the course is automatically marked complete and a `completedAt` timestamp is recorded. The course then moves to the **Completed Courses** tab and the system prompts the student to rate it.

The platform does **not** track watch time, video pause/resume position, or quiz time per question — only topic-level completion. The platform also does **not** issue certificates of completion at this time.

---

## 7. Quizzes — taking, scoring, and retakes

Each course can have one or more quizzes attached. A quiz consists of multiple questions of three possible types:
- **Single-choice**: one correct option from a list.
- **Multiple-choice**: multiple correct options (checkboxes); the student must pick all correct ones.
- **Text answer**: free text; matched case-insensitively against the instructor's answer.

### Quiz rules
- A quiz only appears on the student's **Available Quizzes** tab once it is **published** by the instructor AND the student is enrolled in the parent course.
- Each quiz has a **passing percentage** (default **70%**) and a **max attempts** count (default **1**).
- Quizzes can have an optional **deadline**. After the deadline passes the quiz is hidden from the student's available list.
- During the attempt the student answers one question at a time and can jump between questions using the question navigator.
- If a deadline is set, a countdown timer is shown and the quiz **auto-submits when time expires**.

### Scoring
The score is calculated as the percentage of correctly-answered questions. A student passes if their score is greater than or equal to the quiz's passing percentage. After submission the student sees their score (if `showScoreToStudent` is enabled by the instructor), pass/fail status, and the time spent.

### Retakes
A student can re-attempt a quiz up to `maxAttempts` times. Once all attempts are used the button changes to **Max Attempts Reached** and the quiz cannot be taken again. All past attempts are listed on the **Completed Quizzes** tab with their scores.

---

## 8. Ratings and reviews

A student can rate a course only **after they complete it** (progress = 100%). When a completed course is unrated, the **Completed Courses** tab shows a "Pending Rating" alert. The rating form collects three things:
- **Course rating** (1 to 5 stars)
- **Instructor rating** (1 to 5 stars)
- **Optional comment** (free text)

Each student can submit only **one rating per course**. The course's displayed star rating is the average of all student ratings. Submitting a rating is optional but recommended — it helps other students choose courses and helps instructors improve.

---

## 9. Profile management

The **Profile** page lets a student edit:
- Full name
- Phone number
- Gender
- Date of birth (no future dates allowed)
- Address
- Interests (tag list)
- Profile picture (image upload with preview)
- Dark mode preference (persisted locally)
- Notification preferences (email, SMS, in-app)
- Preferred language and font size

Email is set at signup and **cannot be changed** from the Profile page. Instructors have an additional **Instructor Profile** with fields for bio, qualifications, LinkedIn / portfolio / GitHub / Twitter links, subject expertise tags, availability slots, and two-factor authentication toggle.

---

## 10. Complaints

If a student has a problem — a broken video, a confusing quiz, a billing-style issue, harassment, or anything else — they can file it from the **Complaints** tab of their Student Dashboard. The student writes the complaint as free text and submits it. The complaint appears on the Admin Dashboard's **Complaints** tab as "Pending".

An admin can mark a complaint **Solved** and attach an optional feedback message that becomes visible to the student. There is no priority field, no escalation path, and no SLA — admins resolve complaints in the order they choose.

---

## 11. Student Dashboard — tab-by-tab tour

The Student Dashboard has nine tabs:
1. **Dashboard** — Welcome banner plus KPI cards (enrolled count, completed count, available courses, available quizzes) and a recent activity feed.
2. **Enrolled Courses** — All courses the student is currently enrolled in, each with a progress bar and a Continue Learning button.
3. **Completed Courses** — Courses at 100% progress, with a Pending Rating prompt if not yet rated.
4. **Browse Courses** — All other available courses with Enroll buttons.
5. **Available Quizzes** — Quizzes the student is eligible to take right now.
6. **Completed Quizzes** — All past quiz attempts with score and pass/fail status.
7. **Performance** — The Student Own Performance Dashboard, with charts of course progress and quiz scores over time.
8. **Profile** — Edit personal details and preferences.
9. **Complaints** — File a new complaint and view past ones with their resolution status.

---

## 12. Instructor capabilities (Instructor Dashboard)

Instructors have eight tabs on their dashboard: Dashboard (KPIs), Platform Courses (browse), My Courses (own list with edit/delete), **Create Course**, Students (enrollment list per course, click to view a student's analytics), **Quizzes** (create / edit / publish / extend deadlines), Analytics (course-level performance metrics), and Profile.

When creating a course an instructor provides: title, description, thumbnail URL, duration, content topics (each with a topic name, video URL, and description), optional materials (text or PDF), and a published flag. Courses start as **draft** (`published: false`) and become visible to students only after the instructor sets them published.

When building a quiz the instructor selects the parent course, writes a quiz title and description, and adds questions one at a time. For each question they pick the type (single / multiple / text), write the prompt, define the options, and mark the correct answer. They can also set the passing percentage, max attempts, deadline, and whether to show the score to students.

---

## 13. Admin capabilities (Admin Dashboard)

Admins have four tabs: Dashboard (platform KPIs), **User Directory** (lists of instructors and students with verify / remove actions, plus a drill-down view of students enrolled under a particular instructor), Global Courses (delete any course), and Complaints (resolve and reply to user-filed complaints).

Removing an instructor cascades to delete all the courses they created. Removing a student deletes their account and their enrollments. These actions cannot be undone from the UI.

---

## 14. The Tara AI assistant (this chatbot)

Tara is the floating green chat button on the bottom-right of every page. Clicking it opens the chat window. Tara is powered by a Retrieval-Augmented Generation (RAG) backend that searches this knowledge base for context before answering each question. Tara can:
- Answer questions about how to use the platform.
- Recommend courses based on the user's interests.
- Explain how enrollment, quizzes, ratings, and progress work.
- Read messages aloud (text-to-speech) and copy any reply to clipboard.

Tara cannot:
- Enroll a user in a course (the user must do that themselves).
- Reset a password or change account settings.
- See the user's private data — Tara does not have access to the user's account.
- Issue certificates or grade quizzes.

The first response of a session may take **30–60 seconds** because the backend wakes up from sleep on the free hosting tier. Subsequent responses are fast.

---

## 15. Complete course catalog (22 courses)

Each course has 5 topics, runs in the durations shown below, and is taught by one of the platform's six instructors.

### Foundational programming
- **Programming in C: Foundational Mechanics** — Memory management, pointers, and lower-level architecture. 8 hours. Instructor: S V Devisriprasad. **Mandatory.**
- **Introduction to Python Core Syntax** — Scripting fundamentals, OOP, core data types. 6 hours. Instructor: S V Devisriprasad. **Mandatory.**
- **Java Programming Foundations** — Strictly typed OOP with JVM internals, collections, exceptions, and threads. 10 hours. Instructor: S Sasipratheek. **Mandatory.**

### Data structures and algorithms
- **Data Structures & Algorithms in Python** — Big-O, linked lists, stacks, queues, BSTs, graph algorithms. 12 hours. Instructor: S V Devisriprasad.
- **Advanced Data Structures & Graph Theory** — Self-balancing trees, heaps, network flow, Dijkstra, tries. 10 hours. Instructor: S V Devisriprasad.

### Machine learning and AI
- **Foundations of Statistical Machine Learning** — Supervised learning, regression, classification, clustering, model metrics with NumPy and Scikit-Learn. 15 hours. Instructor: S V Devisriprasad.
- **Deep Learning Architectures & Neural Nets** — Perceptrons, backprop, CNNs, LSTMs, regularization with PyTorch. 14 hours. Instructor: S V Devisriprasad.
- **Natural Language Processing Engine Design** — Tokenization, TF-IDF, word embeddings, sequence-to-sequence, attention and Transformers. 11 hours. Instructor: S V Devisriprasad.
- **Advanced LLMs & Custom RAG Pipelines** — LLM architecture, context injection, vector embeddings, RAG orchestration, AI guardrails. 16 hours. Instructor: S V Devisriprasad.
- **Computer Vision: Edge Analysis to YOLO Models** — OpenCV pixel tensors, spatial filters, feature detection, real-time object recognition. 13 hours. Instructor: S V Devisriprasad.
- **Reinforcement Learning & Agent Deciders** — Markov decision processes, Q-learning, Deep Q-Networks, policy gradients, exploration tradeoffs. 12 hours. Instructor: B Harish.
- **Time-Series Analytics & Forecasting Data Models** — Stationarity, ARIMA, multivariate sequences, seasonality, anomaly detection. 9 hours. Instructor: S V Devisriprasad.

### Web and full-stack development
- **Java Full-Stack: Spring Boot Core Architecture** — IoC and DI, REST controllers, Spring Data JPA, transactions, Spring Security with JWT. 14 hours. Instructor: K Pawan.
- **MERN Stack: Express Server Blueprints** — Node event loop, Express routing, custom middleware, Mongoose, error handling. 11 hours. Instructor: S V Devisriprasad.
- **React Frontend State Management Deep Dive** — Context architecture, custom hooks, Redux, reducers and slices, server cache sync. 12 hours. Instructor: S V Devisriprasad.

### Engineering, operations and infrastructure
- **MLOps: Deployment & Pipeline Tracking Models** — Docker, async APIs, distributed deployment, experiment tracking, drift monitoring. 11 hours. Instructor: S V Devisriprasad.
- **Data Engineering: ETL Pipeline Design Patterns** — Spark, Airflow DAGs, Kafka streaming, warehouse schemas, CDC. 14 hours. Instructor: G Vamil.
- **DevOps: Continuous Integration Core Frameworks** — Git hooks, GitHub Actions, Terraform, Kubernetes, Prometheus monitoring. 10 hours. Instructor: S Sasipratheek.
- **Cloud Computing Systems Architecture** — VPCs, serverless functions, distributed storage, API gateway, IAM. 11 hours. Instructor: K Pawan.

### Security and software engineering practice
- **Cybersecurity Risk & Network Cryptography** — Symmetric / asymmetric ciphers, TLS handshakes, OWASP Top 10, OAuth2 / SAML, network packet inspection. 13 hours. Instructor: S Sasipratheek.
- **Software Engineering Methodologies & Testing** — Unit testing, integration tests, end-to-end automation, SOLID principles, static analysis. 10 hours. Instructor: B Mahesh.

### Recommendations by background
- **New to programming?** Start with *Programming in C*, then *Introduction to Python*, then *Data Structures & Algorithms in Python*.
- **Want to become a web developer?** *MERN Stack: Express Server Blueprints* + *React Frontend State Management Deep Dive*. Add *Java Full-Stack: Spring Boot* if you prefer Java.
- **Want to break into AI/ML?** Start with *Statistical Machine Learning*, then *Deep Learning*, then *NLP*, then *Advanced LLMs & Custom RAG Pipelines*.
- **Interested in deployment and ops?** *Cloud Computing Systems Architecture*, *DevOps CI Core Frameworks*, *MLOps*.

---

## 16. Instructors directory

- **S V Devisriprasad** — Lead instructor. Teaches programming, data structures, machine learning, deep learning, NLP, LLMs, computer vision, time-series, MERN, React, and MLOps.
- **S Sasipratheek** — Teaches Java foundations, DevOps CI, and cybersecurity.
- **K Pawan** — Teaches Java full-stack (Spring Boot) and cloud computing architecture.
- **B Harish** — Teaches reinforcement learning.
- **G Vamil** — Teaches data engineering (Spark, Airflow, Kafka).
- **B Mahesh** — Teaches software engineering methodologies and testing.

---

## 17. What the platform does NOT currently support

To avoid making things up, here is what is **not yet built**:
- Completion certificates (no PDF certificate is issued when a course is finished).
- Paid courses, subscriptions, or any billing system.
- Discussion forums, comments on lessons, or peer-to-peer chat.
- Live classes, scheduled video meetings, or webinars.
- Direct video upload by instructors (videos must be hosted on YouTube and embedded by URL).
- In-app, email, or SMS notifications for new courses, enrollments, or quiz reminders (only OTP emails are sent).
- Badges, points, leaderboards, or gamification.
- Course wishlist or save-for-later.
- Search bar or category filter on the course list.
- A way for students to un-enroll themselves (this requires an admin).
- Editing a quiz attempt after submission.
- Peer review of assignments.

If a user asks about any of the above, tell them it is not currently available and suggest filing a complaint to request the feature.

---

## 18. Frequently asked questions (verbatim)

**Q: How do I sign up?**
A: Click Sign Up on the home page, fill in your name, email, password, and role, then click Send OTP. You will receive a 6-digit code by email — enter it within 10 minutes to finish creating your account.

**Q: I didn't receive the OTP. What do I do?**
A: Check your spam folder. If still missing, wait a minute and request a new OTP. OTPs are valid for 10 minutes.

**Q: I forgot my password.**
A: On the Login page click Forgot Password. Enter your registered email, you will receive a 6-digit OTP, then set a new password.

**Q: How much does it cost to enroll in a course?**
A: Nothing. Every course is free.

**Q: Do I get a certificate when I finish a course?**
A: Not at this time. The platform tracks your completion date but does not issue a downloadable certificate yet.

**Q: How do I enroll in a course?**
A: Open your Student Dashboard, go to the Browse Courses tab, find the course you want, and click Enroll.

**Q: How do I un-enroll from a course?**
A: You cannot un-enroll yourself. Please file a complaint from the Complaints tab and an admin will help.

**Q: How is my course progress calculated?**
A: Each course has 5 topics. Your progress is the percentage of topics you have marked complete in the Course Player. Watching the video alone does not mark a topic complete — you must click Mark Complete.

**Q: How do quizzes work?**
A: Once you are enrolled in a course and the instructor publishes a quiz for it, the quiz appears on your Available Quizzes tab. Click Take Quiz, answer the questions, and submit. You pass if your score is at or above the quiz's passing percentage, usually 70%.

**Q: Can I retake a quiz?**
A: Yes, up to the maximum number of attempts the instructor set (default is 1). Each attempt is recorded on your Completed Quizzes tab.

**Q: Why can't I see a quiz that I know exists?**
A: A quiz only appears for you if (a) you are enrolled in the course it belongs to, (b) the instructor has marked it published, and (c) the deadline (if any) has not passed.

**Q: How do I rate a course?**
A: You can rate a course only after you reach 100% progress. Once you do, the Completed Courses tab shows a "Pending Rating" alert. Fill in the course rating, instructor rating, and an optional comment.

**Q: Which courses should I take first?**
A: If you are new to programming, start with *Programming in C*, then *Introduction to Python*, then *Data Structures & Algorithms in Python*. If you want AI/ML, start with *Foundations of Statistical Machine Learning* and progress to *Deep Learning*, *NLP*, and *Advanced LLMs & Custom RAG Pipelines*.

**Q: Who is the lead instructor?**
A: S V Devisriprasad teaches most of the AI, ML, deep learning, NLP, computer vision, MERN, React, and data structures courses.

**Q: How do I become an instructor?**
A: Sign up and choose "instructor" as your role. New instructor accounts may need to be verified by an admin before you can publish courses.

**Q: How do I contact an instructor?**
A: There is no direct messaging feature yet. File a complaint mentioning the instructor's name, or rate the course with a comment — the instructor sees the comment in their analytics.

**Q: How do I report a bug or a problem with a course?**
A: Open your Student Dashboard, go to the Complaints tab, describe the issue, and submit. An admin will review and respond.

**Q: How do I change my password?**
A: Use the Forgot Password flow from the Login page — there is no separate change-password setting in the Profile yet.

**Q: How do I update my profile picture?**
A: Open the Profile tab on your dashboard, click the picture area to upload a new image, and save.

**Q: Does the platform support dark mode?**
A: Yes. Toggle it from your Profile page. The setting is remembered on your device.

**Q: Are my answers saved if I close the quiz midway?**
A: No. A quiz must be submitted in one sitting. Closing the tab loses your in-progress answers and consumes one attempt only if you submit — leaving without submitting does not consume an attempt.

**Q: What happens if the deadline passes while I am still taking a quiz?**
A: The quiz auto-submits with whatever answers you have selected so far. The score is computed from those answers.

**Q: Can I download the course videos?**
A: No. Videos are embedded from YouTube and play in-browser.

**Q: Can I download course materials (PDFs)?**
A: Yes. PDFs and text documents attached to a course are downloadable from the Materials section of the Course Player.

**Q: Who is Tara?**
A: Tara is this AI assistant — the green chat button on the bottom-right. Tara answers questions about the platform using this knowledge base.

**Q: Can Tara enroll me in a course or take a quiz for me?**
A: No. Tara only answers questions. All actions like enrolling, marking topics complete, and taking quizzes have to be done by you.
