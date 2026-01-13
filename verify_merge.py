from data.dummy_data import generate_dummy_data

tailors, orders = generate_dummy_data()

print(f"Total Orders: {len(orders)}")

multi_tailor_orders = [o for o in orders if len(o.tailors_involved) > 1]

print(f"Orders with multiple tailors: {len(multi_tailor_orders)}")

if multi_tailor_orders:
    sample = multi_tailor_orders[0]
    print(f"Sample Order ID: {sample.id}")
    print(f"Product: {sample.product_name}")
    print(f"Tailors Involved: {len(sample.tailors_involved)}")
    print(f"Tailors Data: {sample.tailors_involved}")
else:
    print("No orders with multiple tailors found. Check if data supports merging.")
