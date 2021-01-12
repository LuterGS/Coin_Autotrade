import constant


def get_falling(coin_dict, ratio=constant.FALLING_RATIO):
    buyer, seller = 0.0, 0.0
    for data in coin_dict['bid']:
        buyer += float(data['price']) * float(data['qty'])
    for data in coin_dict['ask']:
        seller += float(data['price']) * float(data['qty'])

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



if __name__ == "__main__":
    print(get_zero(3770000))