STATUS_OPTIONS = (
    ("COMPLETED", "Completed"),
    ("RELEASING", "Releasing"),
    ("PLANNED", "Planned"),
    ("CANCELLED", "Cancelled")
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
    ("comics_Comic", "comic_comic"),
    ("comics_Issue", "comic_issue"),
    ("cartoons_VoiceActor", "cartoon_voiceactor"),
    ("cartoons_Network", "cartoon_network"),
    ("cartoons_Character", "cartoon_character"),
    ("cartoons_Cartoon", "cartoon_series"),
    ("cartoons_Episode", "cartoon_episode"),
    ("cartoons_Team", "cartoon_team")
)

REPORT_OPTIONS = (
    ("comics_Publisher", "comic_publisher"),
    ("comics_Staff", "comic_staff"),
    ("comics_Comic", "comic_comic"),
    ("comics_Issue", "comic_issue"),
    ("cartoons_VoiceActor", "cartoon_voiceactor"),
    ("cartoons_Network", "cartoon_network"),
    ("cartoons_Character", "cartoon_character"),
    ("cartoons_Cartoon", "cartoon_series"),
    ("cartoons_Episode", "cartoon_episode"),
    ("cartoons_Team", "cartoon_team"),
    ("cartoons_Location", "cartoon_location"),
    ("users_Thought", "users_thought"),
    ("users_Comment", "users_comment"),
    ("auth_User", "auth_user"),
)

REQUEST_STATUS = (
    ("NONE", "None"),
    ("ACCEPTED", "Accepted"),
    ("REJECTED", "Rejected")
)

CHARACTER_STATUS = (
    ("UNKNOWN", "Unknown"),
    ("ALIVE", "Alive"),
    ("DECEASED", "Deceased")
)

ALIGNMENT_OPTIONS = (
    ("ANTI-HERO", "Anti-Hero"),
    ("GOOD", "Good"),
    ("EVIL", "Evil")
)

def util_calculate_age(dob, dod) -> int:
    return dod.year - dob.year - ((dod.month, dod.day) < (dob.month, dob.day))
