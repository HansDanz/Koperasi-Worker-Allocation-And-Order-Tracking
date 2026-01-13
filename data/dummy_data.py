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
    ]

from models.order import Order

def get_dummy_orders():
    return [
        Order(
            id=101,
            product_name="School Uniform",
            client_name="SDN Surabaya 3",
            quantity_required=100,
            quantity_completed=45,

            tailors_involved={
                1: 20,  # Ibu Sari
                2: 15,  # Ibu Lina
                3: 10,  # Ibu Rini
            },
            unit_price=15000,
            deadline_date="2024-02-15",
            complexity_score=7
        ),
        Order(
            id=102,
            product_name="Batik Shirt",
            client_name="Local Retailer A",
            quantity_required=50,
            quantity_completed=50,
            tailors_involved={
                3: 50,
            },
            unit_price=25000,
            deadline_date="2024-01-20",
            complexity_score=8
        ),
        Order(
            id=103,
            product_name="Prayer Garment",
            client_name="Community Group",
            quantity_required=80,
            quantity_completed=10,
            tailors_involved={
                1: 10,
            },
            unit_price=12000,
            deadline_date="2024-03-01",
            complexity_score=5
        ),
    ]
