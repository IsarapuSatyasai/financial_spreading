# Databricks notebook source
# DBTITLE 1,Title and Overview
# MAGIC %md
# MAGIC ##### Copy Azure Blob Storage to UC Volume
# MAGIC

# COMMAND ----------

STORAGE_ACCOUNT_NAME = "mscstagailtuprd03"
FOLDER_NAME = "projects"
TENANT_ID = "07751f8b-9617-49d5-9024-85f034f400ec"
DBR_MI = "fa515616-7575-408d-8196-320484b017c7"

storage_host = f"{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net"


spark.conf.set(f"fs.azure.account.auth.type.{storage_host}", "OAuth")
spark.conf.set(
    f"fs.azure.account.oauth.provider.type.{storage_host}",
    "org.apache.hadoop.fs.azurebfs.oauth2.MsiTokenProvider",
)
spark.conf.set(
    f"fs.azure.account.oauth2.msi.tenant.{storage_host}",
    TENANT_ID,
)
spark.conf.set(
    f"fs.azure.account.oauth2.client.id.{storage_host}",
    DBR_MI,
)

# COMMAND ----------

source_path = f"abfss://{FOLDER_NAME}@{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net"

# COMMAND ----------


blob_prefix = "/FinancialSpreading/InputData"
if blob_prefix:
    source_path = f"{source_path}/{blob_prefix.strip('/')}"

# COMMAND ----------

volume_path="/Volumes/private_gailtu_prd/dev_srivastavas_gailtu-financialspreading-personal/ground_truth_data"

# COMMAND ----------

print(f"Copying from: {source_path}")
print(f"          to: {volume_path}")

# COMMAND ----------

dbutils.fs.cp(source_path, volume_path, recurse=True)

# COMMAND ----------

# ─------------ Verify -----------------------------------
copied_files = dbutils.fs.ls(volume_path)
print(f"\nDone — {len(copied_files)} items now in {volume_path}:")
for f in copied_files:
    print(f"  {f.name}  ({f.size:,} bytes)")

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Keep Credit lens spreads in ground truth data location

# COMMAND ----------

import tqdm

def list_all_files_recursive(path):
    """Recursively list all files under the given path, traversing subfolders."""
    all_files = []
    for item in dbutils.fs.ls(path):
        if item.name.endswith("/"):  # It's a folder
            all_files.extend(list_all_files_recursive(item.path))
        else:
            all_files.append(item)
    return all_files

# COMMAND ----------

# Recursively list all files in the volume path (including inside folders)
all_files = list_all_files_recursive(volume_path)

# Filter to PDF files that do NOT contain 'creditlens' in their lowercase name
files_to_remove = [
    f for f in all_files
    if f.name.lower().endswith(".pdf") and "creditlens" not in f.name.lower()
]

print(f"Total files (recursive): {len(all_files)}")
print(f"PDF files to remove (no 'CreditLens' in name): {len(files_to_remove)}")

for f in tqdm.tqdm(files_to_remove, desc="Removing non-CreditLens PDFs"):
    dbutils.fs.rm(f.path)

print(f"\nDone — removed {len(files_to_remove)} PDF files.")

# COMMAND ----------

all_files

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Remove files that exist in ground_truth_data volume from input_data

# COMMAND ----------

# Path to input_data volume
input_data_path = "/Volumes/private_gailtu_prd/dev_srivastavas_gailtu-financialspreading-personal/input_data"

# Get all files in ground_truth_data
ground_truth_files = list_all_files_recursive(volume_path)
ground_truth_names = {f.name for f in ground_truth_files}

# Get all files in input_data
input_data_files = list_all_files_recursive(input_data_path)

# Find files in input_data that also exist in ground_truth_data (by name)
files_to_remove = [f for f in input_data_files if f.name in ground_truth_names]

print(f"Files in ground_truth_data: {len(ground_truth_files)}")
print(f"Files in input_data: {len(input_data_files)}")
print(f"Overlapping files to remove from input_data: {len(files_to_remove)}")

for f in tqdm.tqdm(files_to_remove, desc="Removing overlapping files from input_data"):
    dbutils.fs.rm(f.path)

print(f"\nDone — removed {len(files_to_remove)} files from input_data that existed in ground_truth_data.")

# COMMAND ----------

