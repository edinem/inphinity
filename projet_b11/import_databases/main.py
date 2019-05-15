from projet_b11.import_databases.Pfam import Pfam
from projet_b11.import_databases.ThreeDid import ThreeDid
from projet_b11.import_databases.DomainInteractionUpdater import DomainInteractionUpdater


def update_db():

    inphinity = DomainInteractionUpdater()

    # 3did
    did = ThreeDid()
    if did.has_new_version():
        did.get_interactions()
        inphinity.update_inphinity_database(did.domain_interactions, '3did')

    # Pfam
    pfam = Pfam()
    if pfam.has_new_version():
        pfam.get_interactions()
        inphinity.update_inphinity_database(pfam.domain_interactions, 'iPfam')
