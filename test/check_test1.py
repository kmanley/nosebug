from test1 import test1

d = {
  "name": "Chris",
  "value": 10000,
  "taxed_value": 10000 - (10000 * 0.4),
  "in_ca": True
}

print test1(d)
