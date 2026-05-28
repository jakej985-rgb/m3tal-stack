import os
import json

def parse_simple_yaml(content):
    data = {}
    lines = content.split('\n')
    current_key = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        # Handle list items
        if stripped.startswith('-'):
            val = stripped[1:].strip()
            # Remove quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            # Try to convert ports to integer
            if current_key == 'ports':
                try:
                    val = int(val)
                except ValueError:
                    pass
            if current_key and isinstance(data.get(current_key), list):
                data[current_key].append(val)
            continue
        # Handle key-values
        if ':' in stripped:
            parts = stripped.split(':', 1)
            k = parts[0].strip()
            v = parts[1].strip()
            if v == '':
                if k in ['requires', 'optional', 'ports']:
                    data[k] = []
                    current_key = k
                elif k == 'resources':
                    data[k] = {}
                    current_key = k
                else:
                    current_key = k
            else:
                if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                    v = v[1:-1]
                if current_key == 'resources':
                    data['resources'][k] = v
                else:
                    data[k] = v
                    current_key = None
    return data

def parse_yaml(path):
    with open(path, 'r') as f:
        content = f.read()
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        return parse_simple_yaml(content)

def main():
    base_dir = "stacks"
    if not os.path.exists(base_dir):
        print(f"Error: Base stacks directory '{base_dir}' does not exist.")
        return

    repo_url = "https://raw.githubusercontent.com/jakej985-rgb/m3tal-stacks/main/"
    stacks = []

    for root, dirs, files in os.walk(base_dir):
        if "stack.yml" in files:
            stack_yml_path = os.path.join(root, "stack.yml")
            # Parse YAML metadata
            try:
                meta = parse_yaml(stack_yml_path)
            except Exception as e:
                print(f"Failed to parse {stack_yml_path}: {e}")
                continue

            name = meta.get("name")
            category = meta.get("category")
            if not name or not category:
                print(f"Skipping {stack_yml_path}: name or category missing")
                continue

            # Check if docker-compose.yml exists
            compose_exists = "docker-compose.yml" in files
            if not compose_exists:
                print(f"Warning: docker-compose.yml not found in {root}")

            # Construct URLs based on repo structure
            rel_path = os.path.relpath(root, start=".")
            rel_path_url = rel_path.replace(os.path.sep, '/')
            
            meta["download_url"] = f"{repo_url}{rel_path_url}/docker-compose.yml"
            meta["manifest_url"] = f"{repo_url}{rel_path_url}/stack.yml"

            stacks.append(meta)

    index_data = {
        "stacks": stacks
    }

    with open("index.json", "w") as f:
        json.dump(index_data, f, indent=2)

    print(f"Generated index.json with {len(stacks)} stacks.")

if __name__ == "__main__":
    main()
