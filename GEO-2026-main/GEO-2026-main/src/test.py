import numpy as np
from scipy.optimize import differential_evolution
from dataclasses import dataclass
from typing import Dict, List

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
    base_speed: float 

# --- MOCK MODEL ---
class SimpleSpeedModel:
    def __init__(self, tailor_metas: List[Tailor]):
        self.speeds = {t.name: t.base_speed for t in tailor_metas}
    def predict_one(self, name: str, is_custom: bool, qty: int) -> float:
        speed = self.speeds[name]
        if is_custom: speed *= 0.5
        return qty / speed

# --- OPTIMIZER & EVALUATOR ---
class Optimizer:
    def __init__(self, tailors: List[Tailor], X_large=1e4, n_scale=3):
        self.tailors = tailors
        self.X = X_large
        self.n = n_scale
        self.model = None

    def fit(self, model):
        self.model = model

    def evaluate_allocation(self, alloc: Dict[str, int], project: Project):
        """Calculates the cost breakdown for a specific manual allocation"""
        # Convert dict to ordered list of quantities
        quantities = [alloc.get(t.name, 0) for t in self.tailors]
        
        # 1. Masking Check (Custom projects cannot use non-specialists)
        if project.is_custom:
            for i, qty in enumerate(quantities):
                if qty > 0 and not self.tailors[i].is_specialized:
                    return {"total": self.X**self.n, "note": "INVALID: Non-specialist on custom"}

        # 2. Quota Check
        if sum(quantities) != project.quota:
            return {"total": self.X**self.n, "note": f"INVALID: Sum ({sum(quantities)}) != Quota ({project.quota})"}

        # 3. Predict Times
        times = []
        active_names = []
        for i, qty in enumerate(quantities):
            if qty > 0:
                t_i = self.model.predict_one(self.tailors[i].name, project.is_custom, qty)
                times.append(t_i)
                active_names.append(self.tailors[i].name)

        # 4. Penalties
        max_t = max(times) if times else 0
        late_p = 0
        if max_t > project.deadline_hours:
            late_p = (self.X**self.n) + (self.X**(self.n-1) * (max_t - project.deadline_hours))
        
        prox_p = sum([(project.deadline_hours - t)**2 for t in times])
        
        strat_p = 0
        if not project.is_custom:
            strat_p = sum([500 for name in active_names if next(t for t in self.tailors if t.name == name).is_specialized])

        return {
            "total": late_p + prox_p + strat_p,
            "late": late_p,
            "prox": prox_p,
            "strat": strat_p,
            "max_t": max_t,
            "active_count": len(times)
        }

    def _cost_wrapper(self, weights, project):
        """Internal helper for DE solver"""
        if project.is_custom:
            weights = weights * np.array([1 if t.is_specialized else 0 for t in self.tailors])
        if np.sum(weights) == 0: return self.X**self.n
        
        proportions = weights / np.sum(weights)
        quantities = np.floor(proportions * project.quota).astype(int)
        # Fix rounding
        remainder = project.quota - np.sum(quantities)
        if remainder > 0:
            fractions = (proportions * project.quota) - quantities
            for i in np.argsort(fractions)[-int(remainder):]:
                quantities[i] += 1
        
        alloc_dict = {self.tailors[i].name: quantities[i] for i in range(len(self.tailors))}
        return self.evaluate_allocation(alloc_dict, project)["total"]

    def solve(self, project: Project):
        bounds = [(0, 1)] * len(self.tailors)
        res = differential_evolution(self._cost_wrapper, bounds, args=(project,), tol=0.01)
        
        # Convert result to dict
        weights = res.x
        if project.is_custom:
            weights *= np.array([1 if t.is_specialized else 0 for t in self.tailors])
        proportions = weights / np.sum(weights)
        quantities = np.floor(proportions * project.quota).astype(int)
        remainder = project.quota - np.sum(quantities)
        if remainder > 0:
            fractions = (proportions * project.quota) - quantities
            for i in np.argsort(fractions)[-int(remainder):]:
                quantities[i] += 1
        
        best_alloc = {self.tailors[i].name: int(quantities[i]) for i in range(len(self.tailors)) if quantities[i] > 0}
        return best_alloc

# --- COMPARISON SCRIPT ---

def run_comparison(project, tailors, oracle):
    opt = Optimizer(tailors)
    opt.fit(oracle)

    print(f"\n" + "="*80)
    print(f"COMPARISON FOR PROJECT: {project.project_id} ({project.quota} pcs, {project.deadline_hours}h deadline)")
    print("="*80)

    # 1. Optimal Allocation (DE)
    de_alloc = opt.solve(project)
    de_eval = opt.evaluate_allocation(de_alloc, project)

    # 2. Heuristic: Equal Split
    # Only split among specialists if custom
    valid_names = [t.name for t in tailors if (not project.is_custom or t.is_specialized)]
    eq_val = project.quota // len(valid_names)
    eq_alloc = {name: eq_val for name in valid_names}
    # Fix remainder
    eq_alloc[valid_names[0]] += (project.quota - sum(eq_alloc.values()))
    eq_eval = opt.evaluate_allocation(eq_alloc, project)

    # 3. Heuristic: Use Only the "Fastest" person
    fastest = sorted([t for t in tailors if (not project.is_custom or t.is_specialized)], 
                      key=lambda x: x.base_speed, reverse=True)[0]
    fast_alloc = {fastest.name: project.quota}
    fast_eval = opt.evaluate_allocation(fast_alloc, project)

    # PRINT COMPARISON TABLE
    header = f"{'Strategy':<20} | {'Total Cost':<15} | {'Max Time':<10} | {'Late?':<8} | {'Staff':<5}"
    print(header)
    print("-" * len(header))

    def print_row(name, eval_res):
        late_str = "YES" if eval_res.get('late', 0) > 0 else "No"
        total = f"{eval_res['total']:,.2f}"
        print(f"{name:<20} | {total:<15} | {eval_res['max_t']:>8.2f}h | {late_str:<8} | {eval_res.get('active_count',0):<5}")

    print_row("Optimal (DE)", de_eval)
    print_row("Equal Split", eq_eval)
    print_row("Fastest Only", fast_eval)

    print("\nDE ALLOCATION DETAILS:")
    print(de_alloc)

# --- EXECUTE ---
if __name__ == "__main__":
    tailors = [
        Tailor("Alice", is_specialized=True,  base_speed=15.0), 
        Tailor("Bob",   is_specialized=False, base_speed=5.0),  
        Tailor("Charlie", is_specialized=False, base_speed=5.0) 
    ]
    oracle = SimpleSpeedModel(tailors)

    # Case 1: Standard Project
    run_comparison(Project("Standard", 10, 60, False), tailors, oracle)

    # Case 2: Custom Project
    run_comparison(Project("Custom", 10, 30, True), tailors, oracle)