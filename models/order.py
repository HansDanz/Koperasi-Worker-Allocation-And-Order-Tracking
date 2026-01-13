class Order:
    def __init__(
        self,
        id,
        product_name,
        client_name,
        quantity_required,
        placement_date,
        due_date,
        quantity_completed = 0,
        tailors_involved = None,
        ):

        self.id = id
        self.product_name = product_name
        self.client_name = client_name
        self.quantity_required = quantity_required
        self.placement_date = placement_date
        self.due_date = due_date
        self.quantity_completed = quantity_completed
        self.tailors_involved = tailors_involved

    @property
    def status(self):
        if self.quantity_completed >= self.quantity_required:
            return "Completed"
        elif self.tailors_involved == None:
            return "Unassigned"
        else:
            return "In progress"