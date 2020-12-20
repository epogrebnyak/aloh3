# TODO: add requirements

import pytest

from aloh.interface import Product
from aloh.small import OptModel

pa = Product("A")
pa.capacity = 10
pa.unit_cost = 0.1
pa.storage_days = 1
pa.add_order(day=0, volume=1, price=0.2)
pa.requires = dict(В=0.8, C=1)

pb = Product("B")
pb.capacity = 10
pb.unit_cost = 0.1
pb.storage_days = 1
pb.add_order(day=0, volume=0, price=0.2)
pb.requires = dict(C=0.5)

pc = Product("C")
pc.capacity = 10
pc.unit_cost = 0.1
pc.storage_days = 1
pc.add_order(day=0, volume=0, price=0.2)

m = OptModel([pa, pb, pc], model_name="tiny_model", inventory_weight=0.1)
ac, xs = m.evaluate()

print("Orders:", m.accepted_orders())
print("Production:", m.estimated_production())


@pytest.mark.skip(reason="not implemented yet")
def test_all():
    assert ac == {"A": [1], "B": [0], "C": [0]}
    assert xs == {"A": [1], "B": [0.8], "C": [1.5]}


# if __name__ == "__main__":
#    test_all()
