"""
SCSJ4383 - Part B: ORIGINAL ("smelly") version
-----------------------------------------------
A sales-report generator that takes a list of orders and a list of customers
and produces a per-customer summary with discounts and a grand total.

This file intentionally contains several well-known code smells. They are
documented in the project PDF and fixed in ../after/sales_report.py.
"""


def generate_report(orders, customers):
    # ---------------------------------------------------------------
    # SMELL 1: Long Method / God Function.
    # This single function does EVERYTHING: validation, customer lookup,
    # totals, discount logic, category logic, and report formatting.
    #
    # SMELL 2: Duplicated Code.
    # The "line total" and the discount calculation are copy-pasted in
    # more than one place instead of being written once.
    #
    # SMELL 3: Magic Numbers.
    # 0.05, 0.10, 0.15, 1000, 5000 appear with no names or explanation.
    #
    # SMELL 4: Inefficient nested lookup (O(n * m)).
    # For every order we scan the WHOLE customers list to find the name.
    # ---------------------------------------------------------------

    report_lines = []
    grand_total = 0.0
    totals_by_customer = {}

    for o in orders:
        # validation (mixed into the main loop)
        if o["qty"] <= 0:
            continue
        if o["unit_price"] < 0:
            continue

        # SMELL 4: linear search through every customer for each order
        cust_name = "UNKNOWN"
        for c in customers:
            if c["id"] == o["customer_id"]:
                cust_name = c["name"]
                break

        # SMELL 2 + 3: line total computed inline with a magic tax number
        line_total = o["qty"] * o["unit_price"]
        line_total = line_total + (line_total * 0.06)  # 0.06 == tax, magic number

        if o["customer_id"] not in totals_by_customer:
            totals_by_customer[o["customer_id"]] = {"name": cust_name, "total": 0.0}
        totals_by_customer[o["customer_id"]]["total"] = \
            totals_by_customer[o["customer_id"]]["total"] + line_total

    for cid in totals_by_customer:
        t = totals_by_customer[cid]["total"]

        # SMELL 2 + 3: discount tiers, duplicated logic and magic numbers
        if t > 5000:
            discount = t * 0.15
            t2 = t - discount
            tier = "GOLD"
        elif t > 1000:
            discount = t * 0.10
            t2 = t - discount
            tier = "SILVER"
        else:
            discount = t * 0.05
            t2 = t - discount
            tier = "BRONZE"

        grand_total = grand_total + t2
        report_lines.append(
            totals_by_customer[cid]["name"] + " [" + tier + "] : " + str(round(t2, 2))
        )

    report_lines.append("GRAND TOTAL: " + str(round(grand_total, 2)))
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
