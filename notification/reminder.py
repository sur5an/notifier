import csv
from datetime import datetime
import os
from pathlib import Path
from document_db import Documents
from conversation import Conversation
import traceback


class Reminder:

    def __init__(self):
        self.user = None
        self.doc = Documents()

    def remove_reminder(self, data, conversation_id, user):
        input_text = data.split()
        try:
            if input_text is None or len(input_text) != 3:
                response = "`please provide the id of reminder to delete it`"
            else:
                if not self.doc.is_document_present(input_text[2]):
                    response = "`please provide a valid id of reminder to delete it`"
                else:
                    self.doc.delete_document(int(input_text[2]))
                    response = "`deleted successfully`"
        except Exception as e:
            print(e)
            traceback.print_exc()
            response = "`please provide a valid id of reminder to delete it`"

        return response

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
            if str(next_question).lower().find("date") >= 0:
                extra = " (format MM/DD/YYYY - Eg 05/31/2020     will be may 5th of 2020)"
            elif str(next_question).lower() in ["RemindStart", "RemindFrequency"]:
                extra = " (format 1M for 1 month, 3M for 3 Months, 1W for one week, 1Y for one year - " \
                        "only M/W/Y is supported)"
            response = "Please give input for %s%s: " % (next_question, extra)
        return response

    def slack_list(self, data, conversation_id, user):
        input_text = data.split()
        response = "\n"

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
                response += "```Please give doc list <username> With username as one of the below.\n\n" + "\n".join(records) + "```\n\n"
        else:
            recs = self.doc.select_user_records(self.user)
            if recs is None or len(recs) == 0:
                response = "`No reminders - every thing is clean` :beach_with_umbrella:"
            else:
                r, e = Documents().get_records_to_notify(datetime.combine(datetime.today(), datetime.min.time()))
                expire_ids = list()
                for ex_rec in e:
                    print(ex_rec)
                    expire_ids.append(ex_rec["Id"])
                for r in recs:
                    mark_red = False
                    if r["Id"] in expire_ids:
                        mark_red = True
                        response += "*Id*: `%s`\n" % str(r["Id"])
                    else:
                        response += "*Id*: %s\n" % str(r["Id"])
                    for k in r:
                        if k == "Id":
                            continue
                        if mark_red:
                            response += "*%s*: `%s`\n" % (k, str(r[k]))
                        else:
                            response += "*%s*: %s\n" % (k, str(r[k]))
                    if r["Id"] in expire_ids:
                        response += "`"
                    response += "\n"
        return response
