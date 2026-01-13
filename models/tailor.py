class Tailor:
    def __init__(self, id, name, skill_vector, reliability_score, max_capacity, current_workload, availability_hours, employed_since, age=None, phone=None, address=None):
        self.id = id
        self.name = name
        self.skill_vector = skill_vector
        self.reliability_score = reliability_score
        self.max_capacity = max_capacity
        self.current_workload = current_workload
        self.availability_hours = availability_hours
        self.employed_since = employed_since
        
        # New dummy attributes
        self.age = age
        self.phone = phone
        self.address = address

    def calculate_earnings(self, orders):
        total_earnings = 0
        for order in orders:
            # Check if order has 'unit_price' attribute to avoid errors with old data
            price = getattr(order, 'unit_price', 0)
            if order.tailors_involved and self.id in order.tailors_involved:
                assignment_data = order.tailors_involved[self.id]
                
                # Handle both old (int) and new (dict) structures
                if isinstance(assignment_data, int):
                    # Legacy structure: Assume all assigned are "complete" for earnings? 
                    # Or maybe 0? Let's assume assigned = potential earnings, but typically we pay for completion.
                    # For safety in migration, let's assume fully completed if legacy.
                    qty_completed = assignment_data
                elif isinstance(assignment_data, dict):
                    qty_completed = assignment_data.get("completed", 0)
                else:
                    qty_completed = 0
                    
                total_earnings += qty_completed * price
        return total_earnings