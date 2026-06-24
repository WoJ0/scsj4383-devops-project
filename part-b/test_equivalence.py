"""
SCSJ4383 - Part B: behaviour-preservation test
----------------------------------------------
Refactoring must NOT change behaviour. This test runs the original and the
refactored report generator on several datasets and asserts the output is
identical. Run:  python test_equivalence.py
"""

import importlib.util
import os
import random

BASE = os.path.dirname(os.path.abspath(__file__))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


before = load(os.path.join(BASE, "before", "sales_report.py"), "before_mod")
after = load(os.path.join(BASE, "after", "sales_report.py"), "after_mod")


def random_dataset(seed):
    random.seed(seed)
    n = random.randint(5, 50)
    customers = [{"id": i, "name": f"C{i}"} for i in range(n)]
    orders = [{
        "customer_id": random.randint(0, n - 1),
        "qty": random.randint(-2, 20),          # includes invalid qty<=0
        "unit_price": round(random.uniform(-5, 900), 2),  # includes invalid <0
    } for _ in range(random.randint(10, 200))]
    return orders, customers


def run():
    cases = 0
    for seed in range(50):
        orders, customers = random_dataset(seed)
        assert before.generate_report(orders, customers) == \
               after.generate_report(orders, customers), f"Mismatch on seed {seed}"
        cases += 1
    print(f"PASS: original and refactored produced identical output on {cases} datasets.")


if __name__ == "__main__":
    run()
