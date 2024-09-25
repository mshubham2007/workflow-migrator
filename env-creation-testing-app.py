import requests
import jwt
import time
import os

# GitHub App Configuration
APP_ID = os.getenv("APP_ID")  # App ID from the workflow environment variable
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Private Key passed via GitHub Actions secrets
INSTALLATION_ID = os.getenv("INSTALLATION_ID")  # Installation ID passed via GitHub Actions secrets
REPOSITORIES = ["mshubham2007/environments-check", "mshubham2007/CalculatorApp", "mshubham2007/argocd-example-apps"]  # List of repositories extracted from issue form

# Function to generate JWT for GitHub App
def generate_jwt(app_id, private_key):
    current_time = int(time.time())
    payload = {
        'iat': current_time,  # Issued at time
        'exp': current_time + (10 * 60),  # JWT expiration (10 minutes)
        'iss': app_id  # GitHub App ID
    }

    # Use the private key from the environment variable
    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token

# Get installation token for a specific repository
def get_installation_token(jwt_token, installation_id):
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()['token']

# Create an environment in the target repository
def create_environment(repo, token, environment_name):
    url = f"https://api.github.com/repos/{repo}/environments/{environment_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "wait_timer": 0,
        "protection_rules": {
            "required_reviewers": 1
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Environment '{environment_name}' created successfully in {repo}")
    else:
        print(f"Failed to create environment in {repo}: {response.status_code}, {response.text}")

# Add variables to the environment
def add_variable(repo, token, environment_name, variable_name, variable_value):
    url = f"https://api.github.com/repos/{repo}/environments/{environment_name}/variables"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": variable_name,
        "value": variable_value
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Variable '{variable_name}' added successfully to environment '{environment_name}' in {repo}")
    else:
        print(f"Failed to add variable in {repo}: {response.status_code}, {response.text}")

# Main function to run the environment creation process
def main():
    # Step 1: Generate JWT using the private key from environment
    jwt_token = generate_jwt(APP_ID, PRIVATE_KEY)
    
    environment_name = "dev"  # Example environment name
    
    for repo in REPOSITORIES:
        # Step 2: Get installation token for the repository
        installation_token = get_installation_token(jwt_token, INSTALLATION_ID)

        # Step 3: Create the environment
        create_environment(repo, installation_token, environment_name)
        
        # Step 4: Add environment variables
        add_variable(repo, installation_token, environment_name, "DATABASE_URL", "postgres://localhost:5432/mydb")
        add_variable(repo, installation_token, environment_name, "ENVIRONMENT", "development")

if __name__ == "__main__":
    main()
