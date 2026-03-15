import os
import sys

def create_scaffold(feature_name):
    print(f"🚀 Scaffolding feature: {feature_name}...")
    
    # Paths
    backend_path = os.path.join("backend", "app", "api", "endpoints")
    frontend_path = os.path.join("frontend", "components", feature_name)
    
    # 1. Backend Route Boilerplate
    os.makedirs(backend_path, exist_ok=True)
    backend_file = os.path.join(backend_path, f"{feature_name}.py")
    with open(backend_file, "w") as f:
        f.write(f'from fastapi import APIRouter, Depends\n\nrouter = APIRouter()\n\n@router.get("/")\nasync def read_{feature_name}():\n    return {{"message": "Hello from {feature_name}"}}\n')
    
    # 2. Frontend Component Boilerplate
    os.makedirs(frontend_path, exist_ok=True)
    frontend_file = os.path.join(frontend_path, f"{feature_name}.tsx")
    with open(frontend_file, "w") as f:
        f.write(f'\'use client\';\n\nexport default function {feature_name.capitalize()}() {{\n  return (\n    <div className="panel">\n      <h2>{feature_name.capitalize()} Component</h2>\n    </div>\n  );\n}}\n')
    
    print(f"✅ Created backend route: {backend_file}")
    print(f"✅ Created frontend component: {frontend_file}")
    print("\nNext steps: \n1. Register the route in backend/app/main.py\n2. Import the component in your dashboard.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/scaffold.py <feature_name>")
    else:
        create_scaffold(sys.argv[1])
