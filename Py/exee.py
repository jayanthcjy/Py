from faker import Faker

# Create a Faker instance
fake = Faker()

# Generate and print a random latitude
latitude = fake.latitude()
print(f"Random Latitude: {latitude}")
# lat=str(latitude)
print(type(latitude))