import csv
import asyncio

from api.magiceden import fetch_attributes
from config import COLLECTION_SLUG

async def main():
    if not COLLECTION_SLUG:
        print("COLLECTION_SLUG not set in config.py")
        return

    fetched_attributes = await fetch_attributes(COLLECTION_SLUG)
    available_attributes = fetched_attributes.get("results", {}).get("availableAttributes", [])

    # Collect all unique trait types, skipping 'Attributes Count'
    trait_types = set()
    for attr_info in available_attributes:
        attribute = attr_info.get("attribute", {})
        trait_type = attribute.get("trait_type", "")
        if trait_type and trait_type != 'Attributes Count':
            trait_types.add(trait_type)
    trait_types = sorted(trait_types)

    # Prepare a dict for each trait_type with all its values
    trait_values = {trait: [] for trait in trait_types}
    for attr_info in available_attributes:
        attribute = attr_info.get("attribute", {})
        trait_type = attribute.get("trait_type", "")
        value = attribute.get("value", "")
        if trait_type and value and trait_type in trait_values:
            trait_values[trait_type].append(value)

    # Write to CSV: each column is a trait_type, each row is a value (empty if not enough values)
    max_len = max(len(vals) for vals in trait_values.values()) if trait_values else 0
    with open(f"{COLLECTION_SLUG}_traits.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=trait_types)
        writer.writeheader()
        for i in range(max_len):
            row = {trait: trait_values[trait][i] if i < len(trait_values[trait]) else "" for trait in trait_types}
            writer.writerow(row)

# run the main function
if __name__ == "__main__":
    asyncio.run(main())