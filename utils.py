

def seconds_to_time(time):
    minutes = time // 60
    seconds = time - (minutes * 60)

    ret = ""
    if minutes > 0:
        ret += f"{minutes}:"
    ret += f"{seconds:02}"
    return ret

def time_to_seconds(time):
    split = time.split(":")
    try:
        if len(split) == 1:
            return int(split[0])
        else:
            return int(split[0]) * 60 + int(split[1])

    except Exception:
        return -1



if __name__ == "__main__":
    print(seconds_to_time(100))
    print(seconds_to_time(55))
    print(seconds_to_time(125))
    print(time_to_seconds("1:40"))
    print(time_to_seconds("55"))
    print(time_to_seconds("2:05"))
