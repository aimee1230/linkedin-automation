# -----------------------------------
# Calculate engagement score
# -----------------------------------
def convert_time_to_minutes(time_str):

    if not time_str:
        return None

    try:
        value = int(time_str[:-1])
        unit = time_str[-1]

        if unit == "m":
            return value
        elif unit == "h":
            return value * 60
        elif unit == "d":
            return value * 1440
        elif unit == "w":
            return value * 10080
        elif unit == "s":
            return max(1, value / 60)

    except:
        return None
    
def calculate_score(post):

    try:
        likes = int(post["likes"])
        comments = int(post["comments"])
        reposts = int(post["reposts"])
    except:
        return 0

    engagement = likes + (2 * comments) + (3 * reposts)

    #age_minutes = convert_time_to_minutes(post["date"])

    #if not age_minutes or age_minutes == 0:
     #   return engagement

    #trending_score = engagement / age_minutes
    trending_score = engagement

    return trending_score
