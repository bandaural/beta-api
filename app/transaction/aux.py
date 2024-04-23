


def transform_body(body):

    #getting the date
    idx1 = body.index('el ')
    idx2 = body.index('. Re')

    res = ''
    # getting elements in between
    for idx in range(idx1 + len('el ') , idx2):
        res = res + body[idx]

    date = res

    # getting expense
    idx1 = body.index('por ')
    idx2 = body.index(' con')
    res = ''
    # getting elements in between
    for idx in range(idx1 + len('por ') , idx2):
        res = res + body[idx]

    res = res.replace("$","").replace(".","")
    expense = int(res)

    # getting card
    idx1 = body.index('con ')
    idx2 = body.index(' en')

    res = ''
    # getting elements in between
    for idx in range(idx1 + len('con ') , idx2):
        res = res + body[idx]

    card = res

    # getting supplier
    idx1 = body.index('en ')
    idx2 = body.index(' el')

    res = ''
    # getting elements in between
    for idx in range(idx1 + len('en ') , idx2):
        res = res + body[idx]

    supplier = res

    #creating the dict
    dict = {
        'date': date,
        'income': None,
        'expense': expense,
        'card': card,
        'currency': 'CLP',
        'supplier': {
            "name": supplier,
        }
    }

    return dict