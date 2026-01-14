from models.tailor import Tailor
from models.order import Order
import random
from datetime import datetime, timedelta

# --- Generators ---

def generate_tailors(count=50):
    names = [
        "Sari", "Lina", "Rini", "Wati", "Yanti", "Budi", "Dewi", "Tini", "Ratna", 
        "Sri", "Nur", "Eka", "Dwi", "Tri", "Ani", "Siti", "Putri", "Ayu", "Indah",
        "Wulan", "Lestari", "Rahayu", "Murni", "Susanti", "Yuliana", "Agus", "Herry",
        "Joko", "Slamaet", "Bambang", "Supri", "Widya", "Hana", "Maya", "Ria", "Dian",
        "Nina", "Vina", "Tina", "Lisa", "Mona", "Rina", "Siska", "Desi", "Vera", "Lia"
    ]
    family_names = ["Susanti", "Wibowo", "Permata", "Wijaya", "Kusuma", "Santoso", "Saputra", "Pratama", "Hidayat", "Nugroho"]
    
    tailors = []
    for i in range(1, count + 1):
        first = random.choice(names)
        last = random.choice(family_names)
        fullname = f"{first} {last}" if i % 2 == 0 else f"{first}"
        
<<<<<<< Updated upstream
        # Skills
        raw_skills = ["SEWING", "CUTTING", "QC", "PACKING"]
        skills = {}
        for s in random.sample(raw_skills, k=random.randint(1, 3)):
            skills[s] = random.randint(5, 10)
=======
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
>>>>>>> Stashed changes
            
        tailors.append(
            Tailor(
                id=i,
                name=fullname,
                skill_vector=skills,
                reliability_score=round(random.uniform(7.0, 10.0), 1),
                current_workload=random.randint(0, 30), # Some initial workload
                max_capacity=random.randint(40, 60),
                availability_hours=random.randint(20, 40),
                employed_since="2023-01-01"
            )
        )
    return tailors

def generate_orders(tailors, count=10):
    products = ["School Uniform", "Batik Shirt", "Sports Jersey", "Office Blazer", "Pants", "Kebaya", "Face Mask", "Tote Bag"]
    clients = ["SDN 01", "Bank BCA", "Local Club", "Wedding Org", "Gov Office", "Retail Store A", "Boutique B"]
    
    orders = []
    statuses = ["DRAFT", "PROOFING", "MATERIAL_SOURCING", "CUTTING", "SEWING", "DISTRIBUTION", "COMPLETED"]
    
    for i in range(101, 101 + count):
        status = random.choice(statuses)
        qty = random.randint(10, 200)
        
        # Financials
        wage_per_piece = random.choice([5000, 10000, 15000, 25000, 40000])
        budget = qty * wage_per_piece * random.uniform(1.2, 1.5) # Margin
        
        # Completion logic
        qty_completed = 0
        tailors_involved = None
        actual_cost = 0
        
        if status in ["SEWING", "DISTRIBUTION", "COMPLETED"]:
            # Assign some tailors
            assigned_tailors = random.sample(tailors, k=random.randint(2, 5))
            tailors_involved = {}
            total_assigned_so_far = 0
            
            for t in assigned_tailors:
                if total_assigned_so_far >= qty:
                    break
                
                portion = int(qty / len(assigned_tailors))
                done = 0
                
                if status == "COMPLETED":
                    done = portion
                elif status == "SEWING":
                    done = random.randint(0, portion)
                elif status == "DISTRIBUTION":
                    done = portion
                
                tailors_involved[t.id] = {
                    "assigned": portion,
                    "completed": done,
                    "picked_up": True
                }
                total_assigned_so_far += portion
                qty_completed += done
        
        if status == "COMPLETED":
            qty_completed = qty
            actual_cost = budget * random.uniform(0.9, 1.1)
            
        deadline = (datetime.now() + timedelta(days=random.randint(-10, 60))).date()
        
        orders.append(
            Order(
                id=i,
                product_name=random.choice(products),
                client_name=random.choice(clients),
                quantity_required=qty,
                quantity_completed=qty_completed,
                tailors_involved=tailors_involved,
                unit_price=wage_per_piece,
                deadline_date=deadline,
                complexity_score=random.randint(1, 10),
                current_status=status,
                budget=budget,
                actual_cost=actual_cost
            )
        )
        
    return orders

# --- Static Lists for Import ---

dummy_tailors = generate_tailors(50)
dummy_orders = generate_orders(dummy_tailors, 15) # Generate 15 just to be safe

def get_dummy_tailors():
    return dummy_tailors

def get_dummy_orders():
    return dummy_orders
