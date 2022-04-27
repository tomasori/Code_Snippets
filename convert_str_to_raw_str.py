s = '\"\n'
raw_s = s.encode('unicode-escape').decode().replace('\"', '\\\"')
final_s = raw_s.replace(r'\"\n',r'\\\"\n')

print(s)
print(raw_s)
print(final_s)
