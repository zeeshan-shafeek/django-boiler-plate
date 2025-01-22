from dotenv import dotenv_values

# Load variables from the existing .env file
env_vars = dotenv_values(".env")

# Write the keys to .env.example with empty values
with open(".env.example", "w") as example_file:
    for key in env_vars.keys():
        example_file.write(f"{key}=\n")

print(".env.example created successfully!")
