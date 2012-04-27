def link(stack):
    print "link called!"
    return stack[-1]["current"] != True

ctx = {
  'header': lambda stack : "Colors",
  'item': [
      {'name': "red", 'current': True, 'url': "#Red"},
      {'name': "green", 'current': False, 'url': "#Green"},
      {'name': "blue", 'current': False, 'url': "#Blue"}
  ],
  #'link': lambda stack : stack[-1]["currents"] != True,
  'link' : link,
  'list': lambda stack : len(stack[-1]["item"]) != 0,
  'empty': lambda stack : len(stack[-1]["item"]) == 0,
}