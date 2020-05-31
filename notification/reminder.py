import csv
from datetime import datetime
import os
from pathlib import Path
import document_db
from conversation import Conversation


class Reminder:

    def __init__(self):
        self.user = None
        self.doc = document_db.Documents()

    def add_new_reminder(self, data, conversation_id, user):
        if Conversation.is_active_conversation(conversation_id):
            next_question = Conversation.get_open_question_response(conversation_id, str(data))
            if next_question is None:
                self.doc.insert(Conversation.active_con.get(conversation_id))
                del Conversation.active_con[conversation_id]
                response = ":floppy_disk: _Document inserted_"
            else:
                extra = ""
                if next_question == "DateOfExpire":
                    extra = " (format MM/DD/YYYY - Eg 05/31/2020 will be may 5th of 2020)"
                response = "Please give input for %s%s: " % (next_question, extra)
        else:
            Conversation.active_con[conversation_id] = {"command": data}
            for column in self.doc.INSERT_COLUMNS:
                Conversation.active_con[conversation_id][column] = None
            next_question = Conversation.get_open_question_response(conversation_id, None)
            extra = ""
            if next_question == "DateOfExpire":
                extra = " (format MM/DD/YYYY - Eg 05/31/2020 will be may 5th of 2020)"
            response = "Please give input for %s%s: " % (next_question, extra)
        return response

    def slack_list(self, data, conversation_id, user):
        input_text = data.split()
        response = "\n```"

        if input_text is None or len(input_text) == 2:
            self.user = "users"
        else:
            self.user = input_text[2]

        if self.user == "users":
            records = self.doc.select_users()
            if records is None or len(records) == 0:
                response = "`No reminders - every thing is clean` :beach_with_umbrella:"
            else:
                records = [str(rec) for rec in records]
                response += "Please give doc list <username> With username as one of the below.\n\n" + "\n".join(records) + "```\n\n"
        else:
            recs = self.doc.select_user_records(self.user)
            if recs is None or len(recs) == 0:
                response = "`No reminders - every thing is clean` :beach_with_umbrella:"
            else:
                for r in recs:
                    r = [str(rec) for rec in r]
                    response += "\n".join(r) + "```\n\n"

        return response


def write_file(h, data):
    os.rename("db.txt", "db_%s.txt" % str(datetime.now()).replace(" ", "_").replace(":", "_"))
    file_handle = open("db.txt", "w")

    h = [i.strip().replace('"', '') for i in h]
    file_handle.write('"' + "\", \"".join(h) + "\"\n")
    for row in data:
        row = [str(i).replace('"', '').strip() for i in row]

        file_handle.write('"' + "\", \"".join(row) + "\"\n")

    paths = sorted(Path("./").iterdir(), key=os.path.getmtime)
    paths = [p for p in paths if str(p).endswith(".txt") and str(p).startswith("db_")]
    for i in range(0, len(paths)-10):
        os.remove(str(paths[i]))
    print(paths)

    file_handle.close()


def read_file():
    formats = ["%m/%d/%Y", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M", "%m/%d/%Y %H"]
    file_name = 'db.txt'
    heading = list()
    data = list()
    date_index = list()
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            record = dict()
            row = [i.strip().replace('"', '') for i in row]
            if line_count == 0:
                heading = row
                for i in range(0, len(heading)):
                    if str(heading[i]).lower().find("date") >= 0:
                        date_index.append(i)
                line_count += 1
            else:
                line_count += 1
                for i in date_index:
                    for f in formats:
                        try:
                            row[i] = datetime.strptime(row[i].strip().replace('"', ''), f)
                            break
                        except ValueError:
                            continue
                for i in range(0, len(row)):
                    record[heading[i]] = row[i]
                data.append(record)
    return heading, data

