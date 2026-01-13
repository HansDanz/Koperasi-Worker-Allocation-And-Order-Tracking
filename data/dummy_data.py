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
        
        # Skills
        raw_skills = ["SEWING", "CUTTING", "QC", "PACKING"]
        skills = {}
        for s in random.sample(raw_skills, k=random.randint(1, 3)):
            skills[s] = random.randint(5, 10)
            
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
