from app.models.chats import ChatsRead
from app.models.messages import Messages


class ChatResponseAdapter:
    @staticmethod
    def to_frontend_chats(chat: list[ChatsRead]) -> list[dict]:
        converted_chats = []
        for c in chat:
            chat_dict = c.model_dump()
            chat_dict["id"] = str(chat_dict["id"])
            chat_dict["workflowId"] = str(chat_dict["workflow_id"])
            chat_dict.pop("created_at", None)
            chat_dict.pop("updated_at", None)
            chat_dict.pop("workflow_id", None)
            converted_chats.append(chat_dict)
        return converted_chats
    
    @staticmethod
    def to_frontend_messages_with_pagination(message_details)->dict:
        converted_messages=[]
        for m in message_details.get("messages",[]):
            msg_dict=ChatResponseAdapter.to_frontend_message(m)
            converted_messages.append(msg_dict)
        converted_messages.sort(key=lambda x: x["id"])
        message_details["messages"]=converted_messages
        message_details["nextCursor"]=message_details.get("next_cursor")
        message_details.pop("next_cursor",None)
        message_details["totalMessages"]=message_details.pop("total_messages",0)
        message_details["hasMore"]=message_details.pop("has_more",False)
        
        return message_details
    
    @staticmethod
    def to_frontend_message(message: Messages) -> dict:
        msg_dict={}
        msg_dict=message.model_dump()
        msg_dict["id"]=msg_dict["id"]
        msg_dict["chatId"]=str(msg_dict["chat_id"])
        msg_dict["fromEntity"]=msg_dict.pop("from_entity")
        msg_dict.pop("chat_id",None)
        msg_dict.pop("created_at",None)
        msg_dict.pop("updated_at",None)
        return msg_dict