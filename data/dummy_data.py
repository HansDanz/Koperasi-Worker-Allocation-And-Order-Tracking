from models.tailor import Tailor
from models.order import Order


def get_dummy_tailors():
    return [
        Tailor(
            id=1,
            name="Ibu Sari",
            skill_vector={"SEWING": 9, "QC": 7},
            reliability_score=8.5,
            current_workload=20,
            max_capacity=40,
            availability_hours=25,
            employed_since="2022-03-01"
        ),
        Tailor(
            id=2,
            name="Ibu Lina",
            skill_vector={"CUTTING": 8, "SEWING": 6},
            reliability_score=7.8,
            current_workload=15,
            max_capacity=30,
            availability_hours=20,
            employed_since="2023-01-12"
        ),
        Tailor(
            id=3,
            name="Ibu Rini",
            skill_vector={"SEWING": 9.5},
            reliability_score=9.2,
            current_workload=30,
            max_capacity=50,
            availability_hours=30,
            employed_since="2021-09-18"
        ),
        Tailor(
            id=4,
            name="Ibu Wati",
            skill_vector={"SEWING": 7, "QC": 9},
            reliability_score=9.0,
            current_workload=0,
            max_capacity=35,
            availability_hours=20,
            employed_since="2022-06-15"
        ),
         Tailor(
            id=5,
            name="Ibu Yanti",
            skill_vector={"CUTTING": 9, "SEWING": 5},
            reliability_score=8.2,
            current_workload=10,
            max_capacity=45,
            availability_hours=28,
            employed_since="2023-04-01"
        ),
    ]

def get_dummy_orders():
    return [

        Order(
            id=101,
            product_name="School Uniform",
            client_name="SDN Surabaya 3",
            quantity_required=100,
            quantity_completed=45,
            # Update to new structure: {id: {"assigned": x, "completed": y}}
            tailors_involved={
                1: {"assigned": 20, "completed": 20, "picked_up": True}, 
                2: {"assigned": 15, "completed": 15, "picked_up": True}, 
                3: {"assigned": 10, "completed": 10, "picked_up": True}  
            },
            unit_price=15000,
            deadline_date="2024-02-15",
            complexity_score=7,
            current_status="SEWING"
        ),
        Order(
            id=102,
            product_name="Batik Shirt",
            client_name="Local Retailer A",
            quantity_required=50,
            quantity_completed=50,
            tailors_involved={
                3: {"assigned": 50, "completed": 50, "picked_up": True}
            },
            unit_price=25000,
            deadline_date="2024-01-20",
            complexity_score=8,
            current_status="COMPLETED"
        ),
        Order(
            id=103,
            product_name="Prayer Garment",
            client_name="Community Group",
            quantity_required=80,
            quantity_completed=10,
            tailors_involved={
                1: {"assigned": 10, "completed": 10, "picked_up": True} # In progress cutting -> sewing
            },
            unit_price=12000,
            deadline_date="2024-03-01",
            complexity_score=5,
            current_status="SEWING" # Moved to Sewing as Cutting is pre-sewing
        ),
        Order(
            id=104,
            product_name="Company Vest",
            client_name="Tech Corp",
            quantity_required=200,
            quantity_completed=0,
            tailors_involved=None,
            unit_price=35000,
            deadline_date="2024-04-10",
            complexity_score=6,
            current_status="PROOFING"
        ),
        Order(
            id=105,
            product_name="Sports Jersey",
            client_name="Local Club",
            quantity_required=30,
            quantity_completed=0,
            tailors_involved=None,
            unit_price=45000,
            deadline_date="2024-02-28",
            complexity_score=9,
            current_status="DRAFT"
        ),
        Order(
            id=106,
            product_name="Event T-Shirt",
            client_name="Charity Run",
            quantity_required=500,
            quantity_completed=0,
            tailors_involved=None,
            unit_price=10000,
            deadline_date="2024-05-20",
            complexity_score=3,
            current_status="MATERIAL_SOURCING"
        ),
    ]
