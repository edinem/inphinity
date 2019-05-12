from projet_b11.import_databases.Pfam import Pfam
from projet_b11.import_databases.ThreeDid import ThreeDid
from projet_b11.import_databases.DomainInteractionUpdater import DomainInteractionUpdater

inphinity = DomainInteractionUpdater()

# 3did
did = ThreeDid()
did.fetch_version()
did.download_archive()
did.extract_archive()
did.import_sql()
did.fetch_interactions()

#inphinity.update_inphinity_database(did.domain_interactions, '3did')

# Pfam
pfam = Pfam()
pfam.get_interactions()

#inphinity.update_inphinity_database(pfam.domain_interactions, 'Pfam')
