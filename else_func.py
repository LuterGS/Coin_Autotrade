import datetime

import constant


def get_falling(coin_dict, ratio=constant.FALLING_RATIO):
    buyer, seller = 0.0, 0.0
    for data in coin_dict['bid']:
        buyer += float(data['price']) * float(data['qty'])
    for data in coin_dict['ask']:
        seller += float(data['price']) * float(data['qty'])

    # timelog(coin_dict['currency'] + "'s current falling state is - buyer : " + str(buyer) + "\t seller : " + str(seller) + "\t total buyer * ratio : seller - " + str(buyer * ratio) + " : " + str(seller))

    if seller > buyer * ratio:
        return True
    else:
        return False


def get_zero(input_val):
    val = str(int(round(input_val, 0)))
    counter = 0
    for i in range(len(val)):
        if val[-1 + -1 * i] == "0":
            counter += 1
        else:
            break
    return counter


def timelog(*args):
    print(str(datetime.datetime.now()) + "\t", end='')
    print(*args)


def datetime_to_str(date: datetime.datetime):
    return date.strftime("%Y%m%d%H%M%S%f")


def process_sleep():
    i = 0


if __name__ == "__main__":
    timelog("test1", "test2")