from faker import Faker

# Initialize Faker
fake = Faker()

# Number of advertisers to generate
num_advertisers = 300

# Ensure uniqueness using a set
unique_companies = set()

# Generate advertisers
while len(unique_companies) < num_advertisers:
    company_name = fake.company()
    if company_name not in unique_companies:
        unique_companies.add(company_name)

# Print the results without extra whitespace
for company in unique_companies:
    print(company)
