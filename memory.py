import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_memory(user_id, memory):
    data = {
        "user_id": user_id,
        "memory": memory
    }

    return supabase.table("memories").insert(data).execute()


def get_memories(user_id, limit=20):
    response = (
        supabase
        .table("memories")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def delete_memory(memory_id):
    return (
        supabase
        .table("memories")
        .delete()
        .eq("id", memory_id)
        .execute()
    )
