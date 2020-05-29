import csv


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
                if head[cnt].strip() == "User" and element.strip().replace('"', "").lower() != user.replace('"', "").lower():
                    do_add = False
                    break
                resp_row += "\n%s: %s" % (head[cnt].strip(), element.strip())
            cnt += 1
        if do_add:
            resp += resp_row
            resp += "```"
    if user_only:
        resp += "\n".join(users) + "```"
    return resp


def read_file():
    file_name = 'db.txt'
    head = list()
    data = list()

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                head = row
                line_count += 1
            else:
                line_count += 1
                data.append(row)
    return head, data


if __name__ == '__main__':
    print(slack_list("list"))

