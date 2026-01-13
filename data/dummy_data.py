from models.tailor import Tailor
from models.order import Order
import random
import pandas as pd
from datetime import datetime, timedelta

# --- Generators ---

def generate_dummy_data():
    try:
        df = pd.read_excel(r"d:\GEO\Koperasi-Worker-Allocation-And-Order-Tracking\data\geo dummy -2.xlsx")
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return [], []

    # --- 1. Extract Tailors ---
    # Group by Name to get unique tailors and their invariant stats (Specialist)
    tailor_groups = df.groupby("Name")
    
    tailors = []
    tailor_id_map = {}
    
    for idx, (name, group) in enumerate(tailor_groups):
        t_id_str = f"T{idx+100}"
        
        # Get specialty from the first row of this tailor (assuming consistent)
        raw_specialist = group["Specialist"].iloc[0]
        # Map "All" -> Generalist or keep as is. User request: "specialists in Uniforms or generalists who can do All"
        # We will normalize to capitalized strings for display
        if str(raw_specialist).lower() == "all":
            specialty = "Generalist" # Or "All" if preferred, but "Generalist" is clearer for "can do All"
        else:
            specialty = raw_specialist

        # Calculate derived stats from history
        total_items = group["Clothes Assigned"].sum()
        # "Working Time per Clothes (in hours)"
        avg_speed = group["Working Time per Clothes (in hours)"].mean()
        
        # Reliability/Skill simulation based on history
        reliability = 9.0 + (random.random() * 1.0) # High score for existing workers
        
        # Dummy Personal Info
        age = random.randint(22, 55)
        phone = f"08{random.randint(100000000, 999999999)}"
        cities = ["Surabaya"]
        streets = ["Jl. Tunjungan", "Jl. Darmo", "Jl. Pemuda", "Jl. Basuki Rahmat", "Jl. Mayjen Sungkono", "Jl. HR Muhammad", "Jl. Kertajaya", "Jl. Raya Gubeng"]
        address = f"{random.choice(streets)} No. {random.randint(1, 100)}, {random.choice(cities)}"
        
        new_tailor = Tailor(
            id=t_id_str,
            name=name,
            skill_vector={"specialty": specialty}, 
            reliability_score=round(reliability, 1),
            max_capacity=random.randint(40, 60), # Weekly capacity
            current_workload=0,
            availability_hours=random.randint(35, 48), # Weekly hours
            employed_since=2020, # Placeholder
            age=age,
            phone=phone,
            address=address
        )
        
        tailors.append(new_tailor)
        tailor_id_map[name] = t_id_str

    # --- 2. Extract Historical Orders ---
    # We essentially want to MERGE rows that belong to the "same project".
    # Key: (Clothes Category, Clothes Type, Project Start, Project Deadline)
    
    # --- Pricing Logic ---
    def get_pricing(clothes_type, clothes_category):
        # Base pricing model (IDR)
        # Returns: (unit_price, material_cost, wage_per_piece)
        
        # Default (Low complexity)
        unit = 100_000
        material = 60_000
        wage = 30_000
        
        # Adjust based on Category
        if clothes_category == "Custom":
            unit = 350_000
            material = 150_000
            wage = 100_000
        
        # Adjust based on key types
        typ = str(clothes_type).lower()
        if "jacket" in typ:
            unit += 150_000
            material += 80_000
            wage += 40_000
        elif "uniform" in typ:
             # Uniforms are bulk, slightly lower margin per piece but higher qty
             if clothes_category != "Custom":
                 unit = 150_000
                 material = 90_000
                 wage = 40_000
        elif "jersey" in typ:
            unit = 120_000
            material = 70_000
            wage = 35_000

        return unit, material, wage

    projects_map = {}
    
    for i, row in df.iterrows():
        tailor_name = row["Name"]
        t_id = tailor_id_map.get(tailor_name)
        
        qty = int(row["Clothes Assigned"])
        cat = row["Clothes Category"]
        typ = row["Clothes Type"]
        
        start_date = row["Project Start"]
        deadline = row["Project Deadline"]
        
        # Extra Stats
        days_needed = row["Time Needed (in days)"]
        hours_per_piece = row["Working Time per Clothes (in hours)"]
        
        # Convert timestamps to date
        if hasattr(start_date, 'date'): start_date = start_date.date()
        if hasattr(deadline, 'date'): deadline = deadline.date()
        
        # Unique Key for Project
        # Note: We use string formatting for dates to be safe as dict keys
        project_key = (cat, typ, str(start_date), str(deadline))
        
        # Tailor Assignment Payload
        tailor_data = {
            "assigned": qty, 
            "completed": qty, 
            "picked_up": True,
            "days_needed": days_needed,
            "hours_per_piece": hours_per_piece
        }
        
        if project_key in projects_map:
            # Existing Project -> Update
            existing_order = projects_map[project_key]
            
            # Update totals
            existing_order.quantity_required += qty
            existing_order.quantity_completed += qty 
            
            # Update financials (Budget increases with qty)
            # We need to re-calc budget based on new qty
            # We stored unit_price in existing_order, so use it.
            existing_order.budget = existing_order.quantity_required * existing_order.unit_price
            
            # Add or Update tailor
            if t_id in existing_order.tailors_involved:
                # Same tailor exists, merge quantities
                existing_data = existing_order.tailors_involved[t_id]
                existing_data["assigned"] += qty
                existing_data["completed"] += qty
            else:
                existing_order.tailors_involved[t_id] = tailor_data
            
        else:
             # New Project -> Create
            o_id = 1000 + len(projects_map) # Simple incremental ID
            
            # Generate Financials
            unit_p, mat_cost, wage_per = get_pricing(typ, cat)
            total_budget = unit_p * qty
            
            # Helper: We will store material cost in actual_cost for now as a proxy, 
            # or we need to add a field. `actual_cost` in model usually means TOTAL cost.
            # Let's assume actual_cost = Total Material + Total Wages (once assigned).
            # But for initial dummy data, let's just use budget.
            # We will use `unit_price` field to store the REVENUE per piece (Price Client Pays)
            # And we need to store WAGE somewhere. Model has `wage_per_piece` in constructor/init but not mapped?
            # Checked model: `unit_price` comment says "# Worker Wage per piece" in line 40? 
            # Wait, Line 40: self.unit_price = unit_price # Worker Wage per piece
            # That comment seems confusing or wrong if unit_price is usually Client Price.
            # Let's fix the Model usage. 
            # Common sense: unit_price = Client Price. 
            # We need a new field `wage_per_piece` in Order if we want to track it, or just use `complexity_score` map.
            # Let's add `wage_per_piece` to Order dynamically or repurpose.
            # Actually, the user asked for "Price per piece of cloth to wage the worker".
            # Let's assume we can add `wage_per_piece` to the Order object.
            
            new_order = Order(
                id=o_id,
                product_name=f"{typ} ({cat})",
                client_name="Historical Data",
                quantity_required=qty,
                quantity_completed=qty,
                tailors_involved={t_id: tailor_data},
                unit_price=unit_p, 
                deadline_date=deadline,
                current_status="COMPLETED",
                start_date=start_date,
                clothes_category=cat,
                clothes_type=typ,
                budget=total_budget
            )
            # Inject extra fields dynamically since Model might strictly define init but we can add props in Python
            new_order.wage_per_piece = wage_per
            new_order.material_cost_per_piece = mat_cost
            
            projects_map[project_key] = new_order

    # Create temporary list of existing orders
    temp_orders = list(projects_map.values())

    # --- 3. Generate Synthetic "Filler" Orders (for robust Financials) ---
    # Generate ~50 orders spread across 2025
    # Types: Uniform, Jersey, PDH (Bulk items)
    filler_types = [
        ("Uniform", "Uniform Shirt"), ("Uniform", "Uniform Skirt"), 
        ("Custom", "Jersey"), ("Uniform", "PDH")
    ]
    
    start_date_range = datetime(2025, 1, 1)
    end_date_range = datetime(2025, 12, 1)
    
    for _ in range(60): # 60 synthetic orders
        o_id = 1000 + len(projects_map) + 1 + _
        
        # Pick random type
        cat, typ = random.choice(filler_types)
        
        # Random Qty (Bulk is usually 20-100)
        qty = random.randint(20, 150)
        
        # Random Date in 2025
        days_offset = random.randint(0, 330)
        p_start = start_date_range + timedelta(days=days_offset)
        # Duration 10-25 days
        p_duration = random.randint(10, 25)
        p_deadline = p_start + timedelta(days=p_duration)
        
        # Financials
        unit_p, mat_cost, wage_per = get_pricing(typ, cat)
        total_budget = unit_p * qty
        actual_cost_val = (mat_cost + wage_per) * qty # Simple actual cost assumption
        
        # Assign to random tailor (Mock assignment)
        # Just pick one tailor for simplicity or split? stick to 1 for filler.
        t_assigned = random.choice(tailors)
        t_data = {
            "assigned": qty,
            "completed": qty,
            "picked_up": True,
            "days_needed": p_duration,
            "hours_per_piece": 4
        }
        
        new_order = Order(
            id=o_id,
            product_name=f"{typ} ({cat}) - Batch {_}", # Distinct name
            client_name=f"Client {random.randint(100, 999)}",
            quantity_required=qty,
            quantity_completed=qty,
            tailors_involved={t_assigned.id: t_data},
            unit_price=unit_p,
            deadline_date=p_deadline.strftime("%Y-%m-%d"),
            current_status="COMPLETED",
            start_date=p_start.strftime("%Y-%m-%d"),
            clothes_category=cat,
            clothes_type=typ,
            budget=total_budget,
            actual_cost=actual_cost_val
        )
        new_order.wage_per_piece = wage_per
        new_order.material_cost_per_piece = mat_cost
        
        temp_orders.append(new_order)

    # Sort by Start Date Descending (Newest First)
    # Convert dates to datetime for correct sorting if they are strings
    temp_orders.sort(key=lambda x: pd.to_datetime(x.start_date), reverse=True)
    
    # Re-assign IDs sequentially (Newest = Smallest ID)
    final_orders = []
    current_id = 1001
    for order in temp_orders:
        order.id = current_id
        final_orders.append(order)
        current_id += 1
        
    orders = final_orders
    
    # Ensure Tailors are sorted by ID
    tailors.sort(key=lambda x: int(x.id[1:]) if x.id.startswith('T') else 0)

    return tailors, orders

# --- Static Lists for Import ---

dummy_tailors, dummy_orders = generate_dummy_data()

def get_dummy_tailors():
    return dummy_tailors

def get_dummy_orders():
    return dummy_orders
