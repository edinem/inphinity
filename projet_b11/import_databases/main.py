from projet_b11.import_databases.ThreeDid import ThreeDid

did = ThreeDid()

did.fetch_version()
did.download_archive()
did.extract_archive()
did.import_sql()
did.get_interactions()
