ctx = {
    'name': "A Book",
    'authors': ["John Power", "Jamie Walsh"],
    'price':{
        'value': 200,
        'vat': lambda stack : "%.2f" % (stack[-1]['price']['value'] * .2),
        'currency': {
            'symbol': '&euro;',
            'name': 'Euro'
        }
     },
    'availability':{
        'status': True,
        'text': "In Stock"
    },
    'truthy': {
        'zero': 0,
        'notTrue': False
    }
}