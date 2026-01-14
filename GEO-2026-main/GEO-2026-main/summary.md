This is a summary of the **Smart Tailor Allocation Engine** project developed for the KSMB Cooperative.

---

### 1. The Core Objective
To transform a manual, memory-based project assignment process into a **Data-Driven Decision Support System**. The goal is to allocate clothes to 111 tailors in a way that ensures 100% on-time delivery, maximizes workshop safety buffers, and respects individual tailor specializations and human limits (fatigue).

### 2. The System Architecture: "Predict-then-Optimize"
The system is built on two distinct "intelligence" layers:

#### Layer A: The Tailor Oracle (Machine Learning)
*   **The Model:** A **Random Forest Regressor** trained on historical project logs.
*   **The Input:** Tailor Name, Clothes Type, specialist status, and the assigned quantity.
*   **The Logic:** Instead of assuming a fixed speed, the Oracle predicts a **Daily Productivity Rate (Pieces per Day)**. This captures individual skill, clothing complexity, and the **Fatigue Curve** (how speed drops as volume increases).
*   **Flexible Hours:** By focusing on "Pieces per Day," the model respects that tailors work flexible hours at home rather than fixed shifts.

#### Layer B: The "Better Algorithm" (Optimization)
*   **The Engine:** **Differential Evolution**, a global search algorithm.
*   **The Metric ($J$):** We seek to **Maximize Workshop Health**.
    $$J = \sum A_i\left(1 - \frac{\hat{W}_i}{d}\right)^2$$
    *   **$\hat{W}_i$:** Predicted days to finish (from the Oracle).
    *   **$d$:** The project deadline.
    *   **$A_i$:** Strategic weight (Ability).
*   **The Behavior:** The system doesn't just try to be "fast." It tries to maximize the **Safety Buffer**. It pushes assignments so that tailors finish as far before the deadline as possible, creating a "cushion" for emergencies.

---

### 3. Key Operational Rules (The Business Logic)
The system strictly enforces the Cooperative's real-world constraints:
*   **Specialist Protection:** "All Specialists" (experts) are penalized on "Normal" projects to keep them free for complex "Custom" orders.
*   **Hard Wall Deadline:** A massive hierarchical penalty ($X^n$) ensures no tailor is ever assigned a workload that the Oracle predicts will take longer than the calendar allows.
*   **One-at-a-time:** Tailors are "Masked" out of the pool if they are currently working on an active kit.
*   **Manager-in-the-Loop:** The algorithm acts as a "Sandbox." The manager can trigger a "Reschedule" at any time (e.g., when a new WhatsApp order arrives) to see the best way to redistribute remaining work.

---

### 4. Technical Validation
We compared two "Brains" for the system using real dummy data:
*   **Linear Regression:** Failed completely ($R^2 = -3.02$). It could not handle the complex differences between tailor types.
*   **Random Forest:** Succeeded ($R^2 = 0.60$ in random tests). 
*   **Chronological Testing:** When tested on "Future" data (training on Jan-June to predict July-Oct), the model showed an **MAE (Mean Absolute Error) of 2.0 days**.
    *   *Insight:* This tells the manager to always maintain at least a **2-day safety margin** in every schedule.

---

### 5. Summary of Benefits
1.  **Sustainability:** Automatically prevents "Day-to-Night" overwork by modeling utilization-based fatigue.
2.  **Efficiency:** Identifies the smallest, most capable team needed for any surge (e.g., 10,000-piece school uniform seasons).
3.  **Transparency:** Replaces "favoritism" or "memory" with objective data on who is actually the most consistent and neat worker.
4.  **Agility:** Allows the cooperative to react instantly to new orders by recalculating the entire workshop's remaining capacity in seconds.

**Status:** The mathematical logic and Python classes are finalized. The system is ready to be connected to the Cooperative's real Excel databases for live production testing.