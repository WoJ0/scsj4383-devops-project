"""
SCSJ4383 - Part B: REFACTORED ("clean") version
------------------------------------------------
Same behaviour as ../before/sales_report.py, but the code smells have been
removed:

  * Long Method      -> split into small, single-responsibility functions.
  * Duplicated Code  -> line total and discount logic written once.
  * Magic Numbers    -> replaced with named constants.
  * O(n*m) lookup    -> customers indexed once into a dict for O(1) lookup,
                        turning the whole report into an O(n + m) algorithm.

The public function generate_report(orders, customers) returns the SAME
output as the original, so behaviour is preserved (verified by tests).
"""

from dataclasses import dataclass, field

# --- Named constants (was: magic numbers) ---
TAX_RATE = 0.06

GOLD_THRESHOLD = 5000
SILVER_THRESHOLD = 1000

GOLD_DISCOUNT = 0.15
SILVER_DISCOUNT = 0.10
BRONZE_DISCOUNT = 0.05

UNKNOWN_CUSTOMER = "UNKNOWN"


@dataclass
class CustomerTotal:
    name: str
    total: float = 0.0


def is_valid(order):
    """One place that decides whether an order should be counted."""
    return order["qty"] > 0 and order["unit_price"] >= 0


def line_total_with_tax(order):
    """Single definition of a taxed line total (was duplicated inline)."""
    base = order["qty"] * order["unit_price"]
    return base + base * TAX_RATE


def index_customers(customers):
    """Build an id -> name map once, so lookups are O(1) instead of O(m)."""
    return {c["id"]: c["name"] for c in customers}


def accumulate_totals(orders, customer_names):
    """Sum taxed line totals per customer in a single pass (O(n))."""
    totals = {}
    for order in orders:
        if not is_valid(order):
            continue
        cid = order["customer_id"]
        if cid not in totals:
            totals[cid] = CustomerTotal(name=customer_names.get(cid, UNKNOWN_CUSTOMER))
        totals[cid].total += line_total_with_tax(order)
    return totals


def tier_and_discount(total):
    """Single source of truth for the discount tiers (was duplicated)."""
    if total > GOLD_THRESHOLD:
        return "GOLD", GOLD_DISCOUNT
    if total > SILVER_THRESHOLD:
        return "SILVER", SILVER_DISCOUNT
    return "BRONZE", BRONZE_DISCOUNT


def generate_report(orders, customers):
    customer_names = index_customers(customers)
    totals = accumulate_totals(orders, customer_names)

    report_lines = []
    grand_total = 0.0
    for entry in totals.values():
        tier, discount_rate = tier_and_discount(entry.total)
        net = entry.total - entry.total * discount_rate
        grand_total += net
        report_lines.append(f"{entry.name} [{tier}] : {round(net, 2)}")

    report_lines.append(f"GRAND TOTAL: {round(grand_total, 2)}")
    return report_lines


if __name__ == "__main__":
    sample_customers = [
        {"id": 1, "name": "Ara"},
        {"id": 2, "name": "Yaran"},
        {"id": 3, "name": "Hanar"},
    ]
    sample_orders = [
        {"customer_id": 1, "qty": 2, "unit_price": 800.0},
        {"customer_id": 2, "qty": 10, "unit_price": 50.0},
        {"customer_id": 3, "qty": 1, "unit_price": 30.0},
        {"customer_id": 1, "qty": 5, "unit_price": 700.0},
    ]
    for line in generate_report(sample_orders, sample_customers):
        print(line)
