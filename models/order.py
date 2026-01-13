from datetime import datetime


class Order:

    STATUS_FLOW = [
        "DRAFT",
        "PROOFING",
        "MATERIAL_SOURCING",
        "CUTTING",
        "SEWING",
        "DISTRIBUTION",
        "COMPLETED"
    ]

    def __init__(
        self,
        id,
        product_name,
        client_name,
        quantity_required,
        quantity_completed = 0,
        tailors_involved = None,
        unit_price = 0,
        deadline_date = None,
        complexity_score = 5,
        current_status = "DRAFT",
        start_date = None,
        budget = 0,
        actual_cost = 0,
        clothes_category = None,
        clothes_type = None
    ):
        self.id = id
        self.product_name = product_name
        self.client_name = client_name
        self.quantity_required = quantity_required
        self.quantity_completed = quantity_completed
        self.tailors_involved = tailors_involved
        self.unit_price = unit_price # Worker Wage per piece
        self.deadline_date = deadline_date
        self.complexity_score = complexity_score
        
        # New attributes
        self.clothes_category = clothes_category
        self.clothes_type = clothes_type
        
        # Financials
        self.budget = budget
        self.actual_cost = actual_cost
        
        # New Workflow Fields
        if current_status not in self.STATUS_FLOW:
             # Fallback for legacy data
             if quantity_completed >= quantity_required:
                 self._status = "COMPLETED"
             elif tailors_involved:
                 self._status = "SEWING"
             else:
                 self._status = "DRAFT"
        else:
            self._status = current_status
            
        self.start_date = start_date if start_date else datetime.now().strftime("%Y-%m-%d")
        
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status in self.STATUS_FLOW:
            self._status = new_status

    def advance_status(self):
        current_idx = self.STATUS_FLOW.index(self._status)
        if current_idx < len(self.STATUS_FLOW) - 1:
            self._status = self.STATUS_FLOW[current_idx + 1]
            return True
        return False
    
    @property
    def progress_pct(self):
        current_idx = self.STATUS_FLOW.index(self._status)
        return int((current_idx / (len(self.STATUS_FLOW) - 1)) * 100)

    # --- New QC / Progress Tracking Methods ---

    def get_tailor_status(self, tailor_id):
        """
        Returns (assigned_qty, completed_qty, picked_up_bool) for a given tailor.
        """
        if not self.tailors_involved or tailor_id not in self.tailors_involved:
            return 0, 0, False
        
        data = self.tailors_involved[tailor_id]
        if isinstance(data, int):
            return data, 0, False 
        elif isinstance(data, dict):
            return data.get("assigned", 0), data.get("completed", 0), data.get("picked_up", False)
        return 0, 0, False

    def get_tailor_stats(self, tailor_id):
        """
        Returns a dict of extra stats (days_needed, hours_per_piece) for a given tailor.
        """
        if not self.tailors_involved or tailor_id not in self.tailors_involved:
            return {}
        
        data = self.tailors_involved[tailor_id]
        if isinstance(data, dict):
             return {
                 "days_needed": data.get("days_needed"),
                 "hours_per_piece": data.get("hours_per_piece")
             }
        return {}

    def confirm_pickup(self, tailor_id):
        """
        Sets picked_up = True for a tailor.
        """
        if not self.tailors_involved or tailor_id not in self.tailors_involved:
            return False
            
        data = self.tailors_involved[tailor_id]
        
        # Normalize to dict if int
        if isinstance(data, int):
            self.tailors_involved[tailor_id] = {"assigned": data, "completed": 0, "picked_up": True}
        else:
            data["picked_up"] = True
            
        return True

    def update_tailor_progress(self, tailor_id, added_completion):
        """
        Increments the completed quantity for a tailor.
        Returns True if successful, False if invalid.
        """
        if not self.tailors_involved or tailor_id not in self.tailors_involved:
            return False
            
        data = self.tailors_involved[tailor_id]
        
        # Normalize to dict if int
        if isinstance(data, int):
            self.tailors_involved[tailor_id] = {"assigned": data, "completed": 0, "picked_up": False}
            data = self.tailors_involved[tailor_id]
            
        current_completed = data.get("completed", 0)
        max_assigned = data.get("assigned", 0)
        
        new_total = current_completed + added_completion
        
        if new_total > max_assigned:
            return False # Cannot complete more than assigned
            
        data["completed"] = new_total
        
        # Also update global order quantity_completed?
        self._recalculate_global_completion()
        
        return True

    def _recalculate_global_completion(self):
        total_completed = 0
        if self.tailors_involved:
            for tid, data in self.tailors_involved.items():
                if isinstance(data, dict):
                    total_completed += data.get("completed", 0)
        
        self.quantity_completed = total_completed
