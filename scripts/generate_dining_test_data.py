"""Substitute the __DINING__ placeholder in config_files/dining.raw.json and
split the result into per-task files under config_files/dining/.

Run from the WebArena project root:

    python scripts/generate_dining_test_data.py
"""
import json
import os


# Read DINING the same way browser_env.env_config does, but skip importing the
# whole package so this script runs without WebArena's heavy deps installed.
DINING = os.environ.get("DINING", "https://dining.microsoft.com")


def main() -> None:
    in_path = "config_files/dining.raw.json"
    out_dir = "config_files/dining"
    out_combined = "config_files/dining.json"

    with open(in_path, "r") as f:
        raw = f.read()
    raw = raw.replace("__DINING__", DINING)

    with open(out_combined, "w") as f:
        f.write(raw)

    os.makedirs(out_dir, exist_ok=True)
    data = json.loads(raw)
    for item in data:
        with open(f"{out_dir}/{item['task_id']}.json", "w") as f:
            json.dump(item, f, indent=2)
    print(
        f"Generated {len(data)} dining tasks: {out_combined} and "
        f"{out_dir}/{{task_id}}.json"
    )


if __name__ == "__main__":
    main()
