from database import get_rooms_id_by_type, get_room_id_by_capacity


def get_free_rooms(occupied_rooms_id: list, room_type: str):
    free_rooms = []
    for room in get_rooms_id_by_type(room_type):
        if room[0] not in occupied_rooms_id:
            free_rooms.append(room[0])

    return free_rooms


def check_capacity(room_type: str, total_people: int):
    rooms = get_room_id_by_capacity(room_type, total_people)
    print(rooms)

    if len(rooms):
        return True
    else:
        return False
