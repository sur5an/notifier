class Conversation:
    active_con = dict()

    @staticmethod
    def is_active_conversation(con_id):
        if Conversation.active_con.get(con_id) is None:
            return False
        return True

    @staticmethod
    def get_open_question_response(con_id, con_str):
        if con_str is not None:
            active_question = Conversation.active_con[con_id]["active_question"]
            Conversation.active_con[con_id][active_question] = con_str
        questions = Conversation.active_con[con_id]
        for question in questions:
            if questions.get(question) is None:
                Conversation.active_con[con_id]["active_question"] = question
                return question
        Conversation.active_con[con_id]["active_question"] = None
        return None