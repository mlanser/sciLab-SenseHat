# =========================================================
#                M A I N   F U N C T I O N S
# =========================================================
def action_one(v1, v2=None):
    if v1 != v2 and v2 is not None:
        return v2
    else:
        return v1


def action_two(v1, v2):
    return v1 + v2
