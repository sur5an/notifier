import csv
from datetime import datetime
import os
from pathlib import Path
import document_db


def slack_list(inp):
    user_only = False
    user = None
    if inp is None or len(inp) == 1 or inp[1] == "users":
        user_only = True
    else:
        user = inp[1]
    head, data = read_file()
    resp = ""
    if user_only:
        resp += "\n```"
    users = set()
    for row in data:
        cnt = 0
        resp_row = ""
        if not user_only:
            resp_row += "\n```"
        do_add = True
        for element in row:
            if user_only:
                if head[cnt].strip() == "User":
                    users.add(element.strip())
                    do_add = False
            else:
                if head[cnt].strip() == "User" and \
                        element.strip().replace('"', "").lower() != user.replace('"', "").lower():
                    do_add = False
                    break
                resp_row += "\n%s: %s" % (str(head[cnt]).strip(), str(element).strip())
            cnt += 1
        if do_add:
            resp += resp_row
            resp += "```"
    if user_only:
        resp += "\n".join(users) + "```"
    return resp


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
                data.append(row)
    return heading, data


if __name__ == '__main__':
    t, d = read_file()
    document_db.insert_all(d)
