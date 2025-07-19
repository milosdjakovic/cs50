def main():
    time = input("What time is it? ")
    f_time = convert(time)

    if f_time >= 7 and f_time <= 8:
        print("breakfast time")
    elif f_time >= 12 and f_time <= 13:
        print("lunch time")
    elif f_time >= 18 and f_time <= 19:
        print("dinner time")


def convert(time):
    h, m = time.split(":")
    i_h = int(h)
    i_m = int(m)
    f_m = float(i_m / 60)
    return i_h + f_m



if __name__ == "__main__":
    main()
