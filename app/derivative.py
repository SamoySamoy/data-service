from datetime import date, timedelta, datetime


def get_third_thursdays(year):
    third_thursdays = []
    for month in range(1, 13):  # Iterate over months
        # Find the first day of the month
        first_day = date(year, month, 1)
        # Calculate the weekday of the first day (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        first_day_weekday = first_day.weekday()
        # Calculate the offset to reach the third Thursday
        offset = (3 - first_day_weekday + 7) % 7
        # Calculate the third Thursday of the month
        third_thursday = first_day + timedelta(days=offset + 14)
        # Check if the third Thursday falls within the month
        if third_thursday.month == month:
            third_thursdays.append(third_thursday)

    return third_thursdays


def find_nearest_third_thursdays(input_date):
    year = input_date.year
    third_thursdays = get_third_thursdays(year)

    if third_thursdays[-1] < input_date:
        case = get_third_thursdays(year + 1)
        return [
            case[0],
            case[1],
            case[3],
            case[4],
        ]

    else:
        expand = get_third_thursdays(year) + get_third_thursdays(year + 1)
        for i in range(0, len(expand) - 1):
            if expand[i] > input_date:
                index = i
                break

    return [
        expand[index],
        expand[index + 1],
        expand[index + 3],
        expand[index + 6],
    ]


def derivatives(i_date):
    requested_date = datetime.strptime(i_date, "%d/%m/%Y").date()
    expired_date = find_nearest_third_thursdays(requested_date)
    f1mm = expired_date[0].strftime("%m")
    f1my = expired_date[0].strftime("%y")
    f1m = {
        "symbol": f"VN30F{f1my}{f1mm}",
        "code": "VN30F1M",
        "expired_date": expired_date[0].strftime("%d/%m/%Y")
    }

    f2mm = expired_date[1].strftime("%m")
    f2my = expired_date[1].strftime("%y")
    f2m = {
        "symbol": f"VN30F{f2my}{f2mm}",
        "code": "VN30F2M",
        "expired_date": expired_date[1].strftime("%d/%m/%Y")
    }

    f1qm = expired_date[2].strftime("%m")
    f1qy = expired_date[2].strftime("%y")
    f1q = {
        "symbol": f"VN30F{f1qy}{f1qm}",
        "code": "VN30F1Q",
        "expired_date": expired_date[2].strftime("%d/%m/%Y")
    }

    f2qm = expired_date[3].strftime("%m")
    f2qy = expired_date[3].strftime("%y")
    f2q = {
        "symbol": f"VN30F{f2qy}{f2qm}",
        "code": "VN30F2Q",
        "expired_date": expired_date[3].strftime("%d/%m/%Y")
    }
    
    return [f1m, f2m, f1q, f2q]

