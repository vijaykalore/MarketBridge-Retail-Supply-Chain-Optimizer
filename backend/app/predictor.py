from typing import List

# Very small placeholder predictor: moving average of recent quantities per location
# In a real system this would use historical sales/consumption time series and a robust model.

def predict_restock_quantities(recent_quantities: List[int], safety_stock: int = 10) -> int:
    if not recent_quantities:
        return safety_stock
    avg = sum(recent_quantities) / len(recent_quantities)
    # naive: if avg < safety_stock then recommend safety_stock - avg rounded up
    need = max(0, int(round(safety_stock - avg)))
    return need
