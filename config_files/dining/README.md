# Microsoft Dining task suite

A small WebArena-format task suite targeting `dining.microsoft.com`,
authored from the `dining_appgraph.py` / `crawled-v1/dining.yaml`
artifacts in `~/CrawlerSkill`.

## One-time setup

1. Make sure your Edge profile at `~/.dining_context` has an active
   dining.microsoft.com session (sign in once via the regular Edge browser
   pointed at that user-data-dir).

2. Export the session into a Playwright `storage_state` file:

   ```bash
   python3 ~/CrawlerSkill/scripts/export_dining_storage_state.py \
       --out ~/webarena/.auth/dining_state.json
   ```

   Re-run whenever the export is older than the MSAL refresh-token TTL.

3. Set the `DINING` env var (or rely on the default of
   `https://dining.microsoft.com`) and regenerate the task JSONs:

   ```bash
   cd ~/webarena
   DINING=https://dining.microsoft.com python3 scripts/generate_dining_test_data.py
   ```

   That writes `config_files/dining.json` and `config_files/dining/{task_id}.json`.

## Running a task

Use the standard WebArena runner with one of the per-task files, e.g.:

```bash
cd ~/webarena
python3 run.py \
    --instruction_path config_files/dining/9000.json \
    --result_dir results/dining/9000 \
    --provider openai --model gpt-4o
```

## Tasks

| ID    | Intent                                                                                              | Eval        |
|-------|-----------------------------------------------------------------------------------------------------|-------------|
| 9000  | Latte price at Espresso – Caffe Lusso (Building 2)                                                  | string      |
| 9001  | Calories in a Strawberry Banana Almond Smoothie at Espresso – Caffe Lusso                           | string      |
| 9002  | Madras Smoothie price at Espresso – Caffe Lusso                                                     | string      |
| 9003  | Number of stations at Food Hall 4                                                                   | string      |
| 9004  | Meal periods shown for Food Hall 4                                                                  | string      |
| 9005  | Lunch hours at Food Hall 4                                                                          | string      |
| 9006  | Menu categories at Espresso – Caffe Lusso                                                           | string      |
| 9007  | Total of past order #5289050                                                                        | string      |
| 9008  | Item ordered in past order #3926183                                                                 | string      |
| 9009  | Date of past order #5289050                                                                         | string      |
| 9010  | Number of items in the Bakery section at Espresso – Caffe Lusso                                     | string      |
| 9011  | Price difference: Chocolate Croissant vs. Butter Croissant                                          | string      |
| 9012  | Cheapest Hot Coffee at Espresso – Caffe Lusso                                                       | string      |
| 9013  | Open the menu of the only station at Building 92: Espresso                                          | url_match   |
| 9014  | Open the Order History page                                                                         | url_match   |
| 9015  | Number of cafes under the SUBMIXER CAFETERIA building label                                         | string      |

Order-related tasks (9007–9009) depend on the past orders that exist for the
exported user. If you log in as a different user the answers may not match.
