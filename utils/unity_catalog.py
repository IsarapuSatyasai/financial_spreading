# create_volume(
#  catalog_name="private_gailtu_prd",
#  schema_name="dev_srivastavas_gailtu-financialspreading-personal",
#  volume_name="input_data",
#  comment="Volume for storing raw ingestion files",
# )


# set_grants(
#  catalog_name="my_catalog",
#  schema_name="my_schema",
#  table_name="my_table",
#  grants={
#   "john.doe@delagelanden.com": ["SELECT"],
#   "jane.smith@delagelanden.com": ["SELECT", "MODIFY", "ALL PRIVILEGES"],
#  }
# )


# set_tags(
#  catalog_name="my_catalog",
#  schema_name="my_schema",
#  table_name="my_table",
#  tags={
#   "pii": "true",
#   "owner": "finance-team",
#  }
# )


###########################################################################################################################

def create_volume(
 catalog_name: str,
 schema_name: str,
 volume_name: str,
 comment: str = None,
) -> None:
 """
 Create a volume in Unity Catalog.

 Parameters
 ----------
 catalog_name : str
 Name of the catalog where the volume will be created.
 schema_name : str
 Name of the schema where the volume will be created.
 volume_name : str
 Name of the volume to create.
 comment : str, optional
 Description/comment for the volume.
 """

 full_name = f"`{catalog_name}`.`{schema_name}`.`{volume_name}`"

 sql = f"CREATE VOLUME IF NOT EXISTS {full_name}"

 if comment:
    sql += f" COMMENT '{comment}'"

 spark.sql(sql)
 print(f"Volume {full_name} created successfully.")



##########################################################################################################################

def set_tags(
 catalog_name: str,
 schema_name: str,
 table_name: str = None,
 column_name: str = None,
 volume_name: str = None,
 tags: dict = None,
) -> None:
 """
 Set or update tags on a Unity Catalog securable.

 Determines the securable type automatically based on the
 arguments provided:
 - catalog_name only -> CATALOG
 - catalog_name + schema_name -> SCHEMA
 - catalog_name + schema_name + table_name -> TABLE
 - catalog_name + schema_name + table_name + column_name -> COLUMN
 - catalog_name + schema_name + volume_name -> VOLUME

 Setting a tag with an existing key overwrites its value.

 Parameters
 ----------
 catalog_name : str
  Name of the catalog.
 schema_name : str
  Name of the schema. Pass None to tag the catalog.
 table_name : str, optional
  Name of the table. Required when tagging a table or column.
  Cannot be combined with volume_name.
 column_name : str, optional
  Name of the column. Requires table_name.
 volume_name : str, optional
  Name of the volume. Cannot be combined with table_name.
 tags : dict
  Dictionary of tag key-value pairs to set, e.g.
  {"pii": "true", "owner": "finance-team"}.
 """

 if not tags:
  raise ValueError("tags dictionary must be provided and non-empty.")

 if column_name and not table_name:
  raise ValueError("table_name is required when column_name is specified.")

 if table_name and volume_name:
  raise ValueError("table_name and volume_name cannot both be specified.")

 if column_name and volume_name:
  raise ValueError("column_name cannot be used with volume_name.")

 # Determine securable type and fully qualified name
 if column_name:
  securable = "COLUMN"
  full_name = (
   f"`{catalog_name}`.`{schema_name}`."
   f"`{table_name}`.`{column_name}`"
  )
 elif table_name:
  securable = "TABLE"
  full_name = f"`{catalog_name}`.`{schema_name}`.`{table_name}`"
 elif volume_name:
  securable = "VOLUME"
  full_name = f"`{catalog_name}`.`{schema_name}`.`{volume_name}`"
 elif schema_name:
  securable = "SCHEMA"
  full_name = f"`{catalog_name}`.`{schema_name}`"
 else:
  securable = "CATALOG"
  full_name = f"`{catalog_name}`"

 for key, value in tags.items():
  sql = f"SET TAG ON {securable} {full_name} `{key}` = `{value}`"
  spark.sql(sql)

 print(
  f"Successfully set {len(tags)} tag(s) on {securable} {full_name}."
 )


###########################################################################################################################

def set_grants(
 catalog_name: str,
 schema_name: str = None,
 table_name: str = None,
 volume_name: str = None,
 grants: dict = None,
) -> list:
 """
 Set or update privilege grants on a Unity Catalog securable.

 Determines the securable type automatically based on the
 arguments provided:
 - catalog_name only -> CATALOG
 - catalog_name + schema_name -> SCHEMA
 - catalog_name + schema_name + table_name -> TABLE
 - catalog_name + schema_name + volume_name -> VOLUME

 Parameters
 ----------
 catalog_name : str
  Name of the catalog.
 schema_name : str, optional
  Name of the schema. Pass None when targeting the catalog.
 table_name : str, optional
  Name of the table. Cannot be combined with volume_name.
 volume_name : str, optional
  Name of the volume. Cannot be combined with table_name.
 grants : dict
  Dictionary mapping principals (users, groups, or
  service principals) to a list of privileges, e.g.
  {
   "finance-team": ["SELECT", "MODIFY"],
   "analysts": ["SELECT"],
  }.

 Returns
 -------
 list[str]
  The SQL statements that were generated and executed.
 """

 if not grants:
  raise ValueError("grants dictionary must be provided and non-empty.")

 if table_name and volume_name:
  raise ValueError("table_name and volume_name cannot both be specified.")

 # Determine securable type and fully qualified name
 if table_name:
  securable = "TABLE"
  full_name = f"`{catalog_name}`.`{schema_name}`.`{table_name}`"
 elif volume_name:
  securable = "VOLUME"
  full_name = f"`{catalog_name}`.`{schema_name}`.`{volume_name}`"
 elif schema_name:
  securable = "SCHEMA"
  full_name = f"`{catalog_name}`.`{schema_name}`"
 else:
  securable = "CATALOG"
  full_name = f"`{catalog_name}`"

 statements = []
 for principal, privileges in grants.items():
  if isinstance(privileges, str):
   privileges = [privileges]
  for privilege in privileges:
   sql = (
    f"GRANT {privilege} "
    f"ON {securable} {full_name} "
    f"TO `{principal}`"
   )
   statements.append(sql)

 for stmt in statements:
  spark.sql(stmt)

 print(
  f"Successfully applied {len(statements)} "
  f"privilege(s) on {securable} {full_name}."
 )

 return statements


# create_volume(
#  catalog_name="private_gailtu_prd",
#  schema_name="dev_srivastavas_gailtu-financialspreading-personal",
#  volume_name="ground_truth_data",
#  comment="Volume for storing CreditLends spreads",
# )

# set_tags(
#  catalog_name="private_gailtu_prd",
#  schema_name="dev_srivastavas_gailtu-financialspreading-personal",
#  volume_name="ground_truth_data",
#  tags={
#   "team": "AI-Model-Development",
#   "type": "creditlens-reports",
#   "domain": "CRO",
#  }
# )