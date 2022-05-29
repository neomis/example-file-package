import exf
df = exf.read_json('tests/test1.json')
df.to_exf('tests/test2.exf')
