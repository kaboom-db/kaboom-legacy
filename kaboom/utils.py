STATUS_OPTIONS = (
    ("COMPLETED", "Completed"),
    ("RELEASING", "Releasing"),
    ("PLANNED", "Planned")
)

IMG_REQUEST_FIELDS = (
    ("COVER", "Cover"),
    ("BACKGROUND", "Background"),
    ("GENERIC", "Generic"),
    ("LOGO", "Logo"),
    ("SCREENSHOT", "Screenshot")
)

IMG_REQUEST_OPTIONS = (
    ("comics_Publisher", "comic_publisher"),
    ("comics_Staff", "comic_staff"),
    ("comics_Character", "comic_character"),
    ("comics_Comic", "comic_comic"),
    ("comics_Issue", "comic_issue"),
    ("cartoons_VoiceActor", "cartoon_voiceactor"),
    ("cartoons_Network", "cartoon_network"),
    ("cartoons_Character", "cartoon_character"),
    ("cartoons_Cartoon", "cartoon_series"),
    ("cartoons_Episode", "cartoon_episode")
)

IMG_REQUEST_STATUS = (
    ("NONE", "None"),
    ("ACCEPTED", "Accepted"),
    ("REJECTED", "Rejected")
)

def util_calculate_age(dob, dod) -> int:
    return dod.year - dob.year - ((dod.month, dod.day) < (dob.month, dob.day))
