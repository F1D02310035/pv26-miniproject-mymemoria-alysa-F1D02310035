from database.database import (
    insert_entry,
    get_all_entries,
    delete_entry_by_id,
    update_entry as db_update_entry,
    search_by_title
)


class DiaryController:

    def get_entries(self):
        return get_all_entries()

    def add_entry(self, data):
        insert_entry(
            data["tanggal"],
            data["judul"],
            data["isi_catatan"],
            data["kategori"],
            data["mood"]
        )

    def delete_entry(self, entry_id):
        delete_entry_by_id(entry_id)

    def update_entry(self, entry_id, data):
        db_update_entry(
            entry_id,
            data["tanggal"],
            data["judul"],
            data["isi_catatan"],
            data["kategori"],
            data["mood"]
        )

    def search_entries(self, keyword):
        return search_by_title(keyword)