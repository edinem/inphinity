import datetime

from projet_b11.import_databases.Pfam import Pfam
from projet_b11.import_databases.ThreeDid import ThreeDid
from projet_b11.import_databases.DomainInteractionUpdater import DomainInteractionUpdater

last_update_filename = 'last_update_date.txt'


def update_db():

    inphinity = DomainInteractionUpdater()
    updated = False

    # 3did
    did = ThreeDid()
    if did.has_new_version():
        did.get_interactions()
        inphinity.update_inphinity_database(did.domain_interactions, '3did')
        updated = True

    # Pfam
    pfam = Pfam()
    if pfam.has_new_version():
        pfam.get_interactions()
        inphinity.update_inphinity_database(pfam.domain_interactions, 'iPfam')
        updated = True

    if updated:
        with open(last_update_filename, 'w') as f:
            f.writelines(datetime.datetime.today().__str__())


def get_last_update_date():
    try:
        with open(last_update_filename, 'r') as f:
            return f.readline()
    except FileNotFoundError:
        return ''


update_db()
print(get_last_update_date())
