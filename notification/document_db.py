import sqlite3 as lite
from datetime import datetime
from datetime import timedelta


class Documents:
    DB = 'db/documents.db'
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
        try:
            if self.conn is not None:
                if self.do_commit:
                    self.conn.commit()
                else:
                    self.conn.rollback()
        except:
            pass
        finally:
            try:
                self.conn.close()
            except:
                pass

    def execute(self, sql, fetch=True):
        self.cur.execute(sql)
        if fetch:
            return True, self.cur.fetchall()
        else:
            return True

    def create_schema(self):
        self.cur.execute(self.DROP)
        self.cur.execute(self.CREATE)

    def delete(self, doc_id):
        sql = "delete from %s where Id=%s" % (self.TABLE, doc_id)
        self.execute(sql)
        self.conn.commit()

    @staticmethod
    def format_date(in_val):
        formats = ["%m/%d/%Y", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M", "%m/%d/%Y %H", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
        for f in formats:
            try:
                ret_val = datetime.strptime(in_val.strip().replace('"', ''), f)
                return ret_val
            except ValueError:
                continue
        return in_val

    def insert(self, record, commit=True):
        sql = self.INSERT + " VALUES ("
        values = list()
        for col in sorted(self.INSERT_COLUMNS):
            val = str(record.get(col))
            if col.lower().find("date") >= 0 or self.TABLE_DETAILS.get(col).get("type").find("date") >= 0:
                val = str(Documents.format_date(val))
            values.append('"' + val.replace('"', '\"') + '"')
        sql += ", ".join(values) + ")"
        self.execute(sql, False)
        if commit:
            self.conn.commit()

    @staticmethod
    def month_delta(date, delta):
        m, y = (date.month + delta) % 12, date.year + (date.month + delta - 1) // 12
        if not m:
            m = 12
        da = min(date.day, [31,
                            29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][
            m - 1])
        return date.replace(day=da, month=m, year=y)

    def insert_all(self, records):
        for record in records:
            self.insert(record, False)
        self.conn.commit()

    def select_users(self):
        sql = 'select distinct UserName from %s' % self.TABLE

        rc, resp = self.execute(sql)
        records = list()
        for a in resp:
            records.append(a[0])
        return records

    def delete_document(self, doc_id):
        sql = 'delete from %s where Id=%s' % (self.TABLE, doc_id)
        self.execute(sql)
        self.conn.commit()

    @staticmethod
    def should_notify(fn, num, key, bt):
        n = fn
        while n < bt:
            if n == bt:
                return True
            elif key == "M":
                n = Documents.month_delta(n, num)
            elif key == "W":
                n = n + timedelta(days=7 * num)
            elif key == "Y":
                n = Documents.month_delta(n, num * 12)
        if n == bt:
            return True
        return False

    def get_records_to_notify(self, base_time):
        recs = list()
        expired = list()
        sql = '%s' % self.SELECT
        rc, resp = self.execute(sql)
        for y in resp:
            record = dict()
            for i in range(0, len(y)):
                record[self.COLUMNS[i]] = y[i]
            formatted_date = Documents.format_date(y[0])
            if formatted_date <= base_time:
                recs.append(record)
                expired.append(record)
                continue
            expire_num = int(y[5][:-1])
            expire_key = y[5][-1:]
            alert_num = int(y[4][:-1])
            alert_key = y[4][-1:]
            ready_for_notification = False
            first_notification = 0
            if expire_key == "M" and Documents.month_delta(formatted_date, -expire_num) <= base_time:
                ready_for_notification = True
                first_notification = base_time - timedelta(
                    days=(base_time - Documents.month_delta(formatted_date, -expire_num)).days)
            elif expire_key == "W" and (formatted_date - timedelta(days=7 * expire_num)) <= base_time:
                ready_for_notification = True
                first_notification = base_time - timedelta(days=(base_time - (formatted_date - timedelta(days=7 * expire_num))).days)
            elif expire_key == "Y" and Documents.month_delta(formatted_date, -expire_num * 12) <= base_time:
                ready_for_notification = True
                first_notification = base_time - timedelta(
                    days=(base_time - Documents.month_delta(formatted_date, -expire_num * 12)).days)
            if ready_for_notification and Documents.should_notify(first_notification, alert_num, alert_key, base_time):
                recs.append(record)
        return recs, expired

    def is_document_present(self, doc_id):
        sql = 'select * from %s where Id=%s' % (self.TABLE, doc_id)

        rc, resp = self.execute(sql)
        if len(resp) == 0:
            return False
        return True

    def select_user_records(self, user):
        sql = '%s where UPPER(UserName) = UPPER("%s")' % (self.SELECT, user)
        rc, resp = self.execute(sql)
        records = list()
        for k in resp:
            record = dict()
            for i in range(0, len(k)):
                record[self.COLUMNS[i]] = k[i]
            records.append(record)
        return records

    def select_all(self):
        select_sql = '%s order by DateOfExpire desc' % self.SELECT
        rc, resp = self.execute(select_sql)
        records = list()
        for k in resp:
            record = dict()
            for i in range(0, len(k)):
                record[self.COLUMNS[i]] = k[i]
            records.append(record)
        return records


if __name__ == '__main__':
    Documents().create_schema()
    rec = {
        "DocumentName": "test1",
        "DateOfExpire": "07/02/2021",
        "UserName": "Raja",
        "DocumentDescription": "desc",
        "RemindStart": "2Y",
        "RemindFrequency": "1M"
    }
    Documents().insert(rec, True)
    rec = {
        "DocumentName": "test2",
        "DateOfExpire": "06/19/2020",
        "UserName": "Raja",
        "DocumentDescription": "desc",
        "RemindStart": "1M",
        "RemindFrequency": "2W"
    }
    Documents().insert(rec, True)
    rec = {
        "DocumentName": "test3",
        "DateOfExpire": "06/02/2022",
        "UserName": "Raja",
        "DocumentDescription": "desc",
        "RemindStart": "2Y",
        "RemindFrequency": "1M"
    }
    Documents().insert(rec, True)
    rec = {
        "DocumentName": "test4",
        "DateOfExpire": "06/05/2020",
        "UserName": "Raja",
        "DocumentDescription": "desc",
        "RemindStart": "1W",
        "RemindFrequency": "2M"
    }
    Documents().insert(rec, True)
    r = {
        "DocumentName": "test5",
        "DateOfExpire": "06/25/2020",
        "UserName": "Raja",
        "DocumentDescription": "desc",
        "RemindStart": "2W",
        "RemindFrequency": "2Y"
    }
    Documents().insert(rec, True)
    rec = {
        "DocumentName": "test6",
        "DateOfExpire": "06/25/2021",
        "UserName": "Raja",
        "DocumentDescription": "desc",
        "RemindStart": "2Y",
        "RemindFrequency": "2W"
    }
    Documents().insert(rec, True)
    rec = {
        "DocumentName": "test7",
        "DateOfExpire": "06/03/2019",
        "UserName": "Raja",
        "DocumentDescription": "desc",
        "RemindStart": "1Y",
        "RemindFrequency": "2W"
    }
    Documents().insert(rec, True)
    s, d = Documents().get_records_to_notify(datetime.combine(datetime.today(), datetime.min.time()))
    for rec in s:
        print(rec)
