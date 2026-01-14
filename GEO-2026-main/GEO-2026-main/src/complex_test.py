import numpy as np
from scipy.optimize import differential_evolution
from dataclasses import dataclass
from typing import Dict, List, Any

# --- SCHEMAS ---
@dataclass
class Project:
    project_id: str
    deadline_hours: float
    quota: int
    is_custom: bool

@dataclass
class Tailor:
    name: str
    is_specialized: bool
    base_speed: float # Base pieces per hour

# --- ADVANCED MOCK MODEL (Simulates Fatigue and Specialization) ---
class AdvancedOracle:
    def __init__(self, tailor_metas: List[Tailor]):
        self.tailors = {t.name: t for t in tailor_metas}

    def predict_one(self, name: str, is_custom: bool, qty: int, deadline: float) -> float:
        t = self.tailors[name]
        speed = t.base_speed
        
        if is_custom:
            speed *= 0.6  # 40% penalty for complexity
            
        base_time = qty / speed
        
        # --- NEW: Utilization-Based Fatigue ---
        # utilization = How much of the deadline is consumed by base work
        utilization = base_time / deadline
        
        # If utilization is over 70%, stress kicks in
        if utilization > 0.7:
            stress = utilization - 0.7
            # Fatigue multiplier grows quadratically as they approach 100%
            fatigue_multiplier = 1 + (stress ** 2) * 10 
            return base_time * fatigue_multiplier
        
        return base_time
    

# --- THE OPTIMIZER ---
class Optimizer:
    def __init__(self, tailors: List[Tailor], X_large=1e6, n_scale=3):
        self.tailors = tailors
        self.X = X_large
        self.n = n_scale
        self.model = None

    def fit(self, model):
        self.model = model

    def evaluate(self, alloc: Dict[str, int], project: Project):
        quantities = [alloc.get(t.name, 0) for t in self.tailors]
        
        # 1. Custom Specialist Filter
        if project.is_custom:
            for i, q in enumerate(quantities):
                if q > 0 and not self.tailors[i].is_specialized:
                    return {"total": self.X**self.n, "note": "INVALID: Non-spec on custom"}

        # 2. Quota Check
        if abs(sum(quantities) - project.quota) > 0.1:
            return {"total": self.X**self.n, "note": "INVALID: Quota mismatch"}

        # 3. Predict Times (FIXED: Added project.deadline_hours)
        times = []
        active_indices = []
        for i, q in enumerate(quantities):
            if q > 0:
                t_i = self.model.predict_one(
                    self.tailors[i].name, 
                    project.is_custom, 
                    q, 
                    project.deadline_hours
                )
                times.append(t_i)
                active_indices.append(i)
        
        if not times: return {"total": self.X**self.n}

        # 4. Penalties
        max_t = max(times)
        
        # Late Penalty (Hard Wall)
        late_p = 0
        if max_t > project.deadline_hours:
            late_p = (self.X**self.n) + (self.X**(self.n-1) * (max_t - project.deadline_hours))
        
        # Proximity Penalty (Pacer)
        prox_p = sum([(project.deadline_hours - t)**2 for t in times])
        
        # Strategic Penalty (Save Experts)
        strat_p = 0
        if not project.is_custom:
            strat_p = sum([100 for i in active_indices if self.tailors[i].is_specialized])

        return {"total": late_p + prox_p + strat_p, "max_t": max_t, "staff": len(times)}

    def solve(self, project: Project, available_mask: List[int] = None):
        if available_mask is None: available_mask = [1] * len(self.tailors)
        
        def obj(weights):
            # Apply Masking
            masked = weights * available_mask
            if project.is_custom:
                spec_mask = [1 if t.is_specialized else 0 for t in self.tailors]
                masked = [m * s for m, s in zip(masked, spec_mask)]
            
            if sum(masked) == 0: return self.X**self.n
            
            # Normalize to Sum = Quota
            props = np.array(masked) / sum(masked)
            qtys = np.floor(props * project.quota).astype(int)
            rem = project.quota - sum(qtys)
            for i in np.argsort(props * project.quota - qtys)[-int(rem):]: 
                qtys[i] += 1
            
            # Evaluate using the fixed method
            d = {self.tailors[i].name: qtys[i] for i in range(len(self.tailors)) if qtys[i] > 0}
            return self.evaluate(d, project)["total"]

        # Run Search
        res = differential_evolution(obj, [(0, 1)] * len(self.tailors), tol=0.01, popsize=60)
        
        # Final formatting
        masked = res.x * available_mask
        if project.is_custom:
            spec_mask = [1 if t.is_specialized else 0 for t in self.tailors]
            masked = [m * s for m, s in zip(masked, spec_mask)]
            
        props = np.array(masked) / sum(masked)
        qtys = np.floor(props * project.quota).astype(int)
        rem = project.quota - sum(qtys)
        for i in np.argsort(props * project.quota - qtys)[-int(rem):]: qtys[i] += 1
        
        return {self.tailors[i].name: int(qtys[i]) for i in range(len(self.tailors)) if qtys[i] > 0}
    
# --- TEST EXECUTION ---

# Define a larger workshop (10 Tailors)
workshop = [
    Tailor("Alice",   True,  15.0), # Specialist, Fast
    Tailor("Bob",     False, 10.0),  # Standard, Fast
    Tailor("Charlie", False, 10.0),  # Standard, Fast
    Tailor("David",   True,  12.0), # Specialist, High Endurance
    Tailor("Eve",     False, 5.0), # Standard, Slow but never gets tired
    Tailor("Frank",   False, 8.0),  # Standard, Medium, gets tired fast
    Tailor("Grace",   True,  10.0), # Specialist, Medium
    Tailor("Heidi",   False, 7.0), # Standard, Medium
    Tailor("Ivan",    False, 7.0), # Standard, Medium
    Tailor("Judy",    False, 12.0)   # Standard, Very Fast but burns out instantly
]

oracle = AdvancedOracle(workshop)
opt = Optimizer(workshop)
opt.fit(oracle)

def run_complex_test(name, project: Project, mask=None):
    print(f"\n>>> SCENARIO: {name}")
    print(f"Project: {project.quota} pcs, Deadline: {project.deadline_hours}h, Custom: {project.is_custom}")
    alloc = opt.solve(project, available_mask=mask)
    ev = opt.evaluate(alloc, project)
    print(f"Result: {len(alloc)} tailors used. Max finish time: {ev['max_t']:.2f}h")
    for name, q in alloc.items():
        t = oracle.predict_one(name, project.is_custom, q, project.deadline_hours)
        print(f"  - {name:8}: {q:3} pcs (Time: {t:5.2f}h)")

# 1. The School Surge (Massive order, long deadline)
# Expectation: Uses almost everyone to keep pacing steady.
run_complex_test("The School Surge", Project("P_Surge", 40, 800, False))

# 2. The Specialist Bottleneck (Custom order, limited staff)
# Expectation: Alice, David, and Grace must handle the whole load.
run_complex_test("Specialist Bottleneck", Project("P_Spec", 20, 300, True))

# 3. The Fatigue Trap (Medium order, tight deadline)
# Expectation: Instead of giving 100 to Judy (who burns out), it should split it.
run_complex_test("Fatigue Trap", Project("P_Fatigue", 5, 60, False))

# 4. Partial Availability (Some tailors are busy)
# Masking Alice, Bob, and Charlie (the fastest ones)
busy_mask = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1] 
run_complex_test("Fast Tailors are Busy", Project("P_Busy", 15, 100, False), mask=busy_mask)