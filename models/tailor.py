class Tailor:
    def __init__(self, id, name, skill_vector, reliability_score, max_capacity, current_workload, availability_hours, employed_since):
        self.id = id
        self.name = name
        self.skill_vector = skill_vector
        self.reliability_score = reliability_score
        self.max_capacity = max_capacity
        self.current_workload = current_workload
        self.availability_hours = availability_hours
        self.employed_since = employed_since

    def calculate_earnings(self, orders):
        total_earnings = 0
        for order in orders:
            # Check if order has 'unit_price' attribute to avoid errors with old data
            price = getattr(order, 'unit_price', 0)
            if order.tailors_involved and self.id in order.tailors_involved:
                qty_done_by_tailor = order.tailors_involved[self.id]
                total_earnings += qty_done_by_tailor * price
        return total_earnings