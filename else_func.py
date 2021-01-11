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