import sqlite3 as lite


class Documents:
    DB = 'documents.db'
    TABLE = 'documents'
    DROP: str = 'DROP TABLE IF EXISTS %s' % TABLE
    TABLE_DETAILS = {
        "Id": {
            "desc": "uniq id auto incremented used for internal purpose",
            "type": "INTEGER PRIMARY KEY AUTOINCREMENT"
        },
        "DocumentName": {
            "desc": "Document Name - more line single word explanation for document",
            "type": "TEXT"
        },
        "DateOfExpire": {
            "desc": "Document expiring date - It could be reminder expiring date",
            "type": "TEXT"
        },
        "UserName": {
            "desc": "Whom does the document belong to",
            "type": "TEXT"
        },
        "DocumentDescription": {
            "desc": "Details about the document, will be used to send the notification",
            "type": "TEXT"
        },
        "RemindStart": {
            "desc": "When should the remind start",
            "type": "TEXT"
        },
        "RemindFrequency": {
            "desc": "What is the frequency of the reminder",
            "type": "TEXT"
        }

    }

    def create_construct(self):
        create = 'CREATE TABLE %s(' % self.TABLE
        cols = list()
        for k in self.COLUMNS:
            cols.append("%s %s" % (k, self.TABLE_DETAILS.get(k).get("type")))
        create += ", ".join(cols) + ")"
        return create

    def insert_construct(self):
        insert = 'INSERT INTO %s (' % self.TABLE
        cols = list()
        for k in self.INSERT_COLUMNS:
            cols.append("%s" % k)
        insert += ", ".join(cols) + ")"
        return insert

    def select_construct(self):
        select = 'select '
        cols = list()
        for k in self.COLUMNS:
            cols.append("%s" % k)
        select += ", ".join(cols) + " from %s " % self.TABLE
        return select

    def __init__(self):
        self.conn = lite.connect(self.DB)
        self.cur = self.conn.cursor()
        self.do_commit = True
        self.COLUMNS = sorted(self.TABLE_DETAILS)
        tmp = dict(self.TABLE_DETAILS)
        del tmp["Id"]
        self.INSERT_COLUMNS = sorted(tmp)
        self.CREATE = self.create_construct()
        self.INSERT = self.insert_construct()
        self.SELECT = self.select_construct()

    def __del__(self):
        if self.conn is not None:
            try:
                if self.do_commit:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            finally:
                self.conn.close()

    def execute(self, sql, fetch=True):
        self.cur.execute(sql)
        if fetch:
            return True, self.cur.fetchall()
        else:
            return True

    def create_schema(self):
        self.cur.execute(self.DROP)
        self.cur.execute(self.CREATE)

    def insert(self, record, commit=True):
        sql = self.INSERT + " VALUES ("
        values = list()
        for col in sorted(self.INSERT_COLUMNS):
            values.append('"' + record.get(col).replace('"', '\"') + '"')
        sql += ", ".join(values) + ")"
        self.execute(sql, False)
        self.conn.commit()

    def insert_all(self, records):
        for record in records:
            self.insert(record, False)
        self.conn.commit()

    def select_users(self):
        sql = 'select distinct UserName from %s' % self.TABLE

        rc, resp = self.execute(sql)
        records = list()
        for r in resp:
            records.append(r[0])
        return records

    def delete_document(self, doc_id):
        sql = 'delete %s where Id=%s' % (self.TABLE, doc_id)
        self.execute(sql)
        self.conn.commit()

    def is_document_present(self, doc_id):
        sql = 'select * from %s where Id=%s' % (self.TABLE, doc_id)

        rc, resp = self.execute(sql)
        if len(resp) == 0:
            return False
        return True

    def select_user_records(self, user):
        sql = '%s where UserName = "%s"' % (self.SELECT, user)
        print(sql)
        rc, resp = self.execute(sql)
        records = list()
        head_idx = 0
        for r in resp:
            rec = list()
            for i in range(0, len(r)):
                if self.COLUMNS[i] == "Id":
                    head_idx = i
                rec.append("%s: %s" % (self.COLUMNS[i], r[i]))
            t = rec[head_idx]
            rec[head_idx] = rec[0]
            rec[0] = t
            records.append(rec)
        return records


if __name__ == '__main__':
    Documents().create_schema()
