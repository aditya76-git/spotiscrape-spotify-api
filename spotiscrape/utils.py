import base62, re, datetime, pytz

def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    total_seconds = (minutes * 60) + seconds
    return total_seconds


def find_device_id(devices_data, device_type):
    device_ids = ""
    
    for device_id, device_info in devices_data.items():
        if device_info.get("device_type") == device_type:
            device_ids += device_id
    
    return device_ids

def uri_to_gid(uri):
        return hex(base62.decode(uri, base62.CHARSET_INVERTED))[2:].zfill(32)

def gid_to_uri(gid):
        return base62.encode(int(gid, 16), charset=base62.CHARSET_INVERTED).zfill(22)


def get_current_timezone():
    # Get the current time in UTC
    utc_now = datetime.datetime.utcnow()
    
    # Get the user's local timezone
    local_timezone = pytz.timezone(pytz.country_timezones["US"][0])  # Replace with the desired country code
    
    # Convert UTC time to local time
    local_time = utc_now.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    
    return str(local_time.tzinfo).replace("_" , "")

def extract_id(url):
    patterns = [
        (r"/track/([^/?]+)", "trackID"),
        (r"/artist/([^/?]+)", "artistID"),
        (r"/playlist/([^/?]+)", "playlistID"),
        (r"/album/([^/?]+)", "albumID"),
        (r"/user/([^/?]+)", "userID")
    ]

    for pattern, id_type in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return url


def get_timeTag(milliseconds):
    milliseconds = int(milliseconds)
    seconds = int(milliseconds / 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

