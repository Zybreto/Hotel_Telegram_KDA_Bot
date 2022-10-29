from database import get_rooms_id_by_type


def check_capacity(adults: int, children: int):
    if adults + children <= 4:
        return True
    else:
        return False


def get_free_rooms(occupied_rooms_id: list, room_type: str):
    free_rooms = []
    for room in get_rooms_id_by_type(room_type):
        if room[0] not in occupied_rooms_id:
            free_rooms.append(room[0])

    return free_rooms
