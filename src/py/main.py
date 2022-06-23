from swipe_extractor import grab_first, into_swipe_set


if __name__ == "__main__":
    df = grab_first()
    swipe_set = into_swipe_set(df)
    for swipe in swipe_set:
        print(swipe.stringify())
