from src.db import get_conn, release_conn

class LinkedList:
    def __init__(self):
        self.head_id = None  # Можно хранить ID головы в базе или в переменной

    def list_search(self, key):
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                # Поиск по списку
                cur.execute("SELECT id, key, next_id FROM linked_list WHERE prev_id IS NULL OR id=%s", (self.head_id,))
                x_id = self.head_id
                while x_id:
                    cur.execute("SELECT id, key, next_id FROM linked_list WHERE id=%s", (x_id,))
                    record = cur.fetchone()
                    if not record:
                        break
                    if record[1] == key:
                        return record
                    x_id = record[2]
        except Exception as e:
            print(f"Error during search: {e}")
        finally:
            release_conn(conn)
        return None

    def list_insert(self, key, after_id=None):
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO linked_list (key, prev_id, next_id) VALUES (%s, %s, %s) RETURNING id", (key, after_id, None))
                new_id = cur.fetchone()[0]
                if after_id:
                    cur.execute("UPDATE linked_list SET next_id=%s WHERE id=%s", (new_id, after_id))
                    cur.execute("UPDATE linked_list SET prev_id=%s WHERE id=(SELECT next_id FROM linked_list WHERE id=%s)", (new_id, after_id))
                else:
                    self.head_id = new_id
        except Exception as e:
            print(f"Error during insertion: {e}")
        finally:
            release_conn(conn)

    def list_delete(self, x_id):
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT prev_id, next_id FROM linked_list WHERE id=%s", (x_id,))
                prev_id, next_id = cur.fetchone()

                if prev_id:
                    cur.execute("UPDATE linked_list SET next_id=%s WHERE id=%s", (next_id, prev_id))
                if next_id:
                    cur.execute("UPDATE linked_list SET prev_id=%s WHERE id=%s", (prev_id, next_id))
                cur.execute("DELETE FROM linked_list WHERE id=%s", (x_id,))
        except Exception as e:
            print(f"Error during deletion: {e}")
        finally:
            release_conn(conn)
