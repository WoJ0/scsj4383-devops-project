"""
SCSJ4383 - Part B: performance comparison (BONUS task)
------------------------------------------------------
Generates a realistic dataset, runs BOTH the original and the refactored
report generator, checks their output is identical (behaviour preserved),
and times them to show the speed improvement from refactoring.

Run:  python benchmark.py
"""

import random
import time
import importlib.util
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


before = load(os.path.join(BASE, "before", "sales_report.py"), "before_mod")
after = load(os.path.join(BASE, "after", "sales_report.py"), "after_mod")


def make_dataset(num_customers, num_orders, seed=42):
    random.seed(seed)
    customers = [{"id": i, "name": f"Customer{i}"} for i in range(num_customers)]
    orders = []
    for _ in range(num_orders):
        orders.append({
            "customer_id": random.randint(0, num_customers - 1),
            "qty": random.randint(1, 20),
            "unit_price": round(random.uniform(5, 900), 2),
        })
    return orders, customers


def time_it(func, orders, customers, repeats=5):
    best = float("inf")
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(orders, customers)
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    return best, result


def main():
    num_customers = 2000
    num_orders = 50000
    orders, customers = make_dataset(num_customers, num_orders)

    print(f"Dataset: {num_orders:,} orders across {num_customers:,} customers\n")

    t_before, r_before = time_it(before.generate_report, orders, customers)
    t_after, r_after = time_it(after.generate_report, orders, customers)

    identical = (r_before == r_after)
    speedup = t_before / t_after if t_after > 0 else float("inf")

    print(f"Original  (smelly)   : {t_before * 1000:9.2f} ms")
    print(f"Refactored (clean)   : {t_after * 1000:9.2f} ms")
    print(f"Speed-up             : {speedup:9.1f}x faster")
    print(f"Output identical     : {identical}")


if __name__ == "__main__":
    main()
