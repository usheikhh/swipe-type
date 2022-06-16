from swipe_extractor import grab_first, into_swipe_set, unique_sentences


if __name__ == "__main__":
    df = grab_first()
    swipe_set = into_swipe_set(df)
    for key, _ in swipe_set.items():
        print("Key:", key)
    print("Swipe set:", swipe_set["roses_payments_score_panels"])
