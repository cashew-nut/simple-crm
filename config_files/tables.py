import config

active_table_name: str = "studies"
r_tbl_name: str = "study_organisations"
query: str = f"SELECT * FROM {config.schema}.{active_table_name}"