url = 'https://cq.lianjia.com/ershoufang/c3611060982243/'

before = url[0:url.rfind('c', 1)]
after = url[url.rfind('c', 1):]
print(after)
print(before)
full = before + 'pg3'+after
print(full)

after = url[url.rfind('c', 1)+1:-1]

print(after)

url = 'https://wh.lianjia.com/ershoufang/104103118075.html'

house_id = url[url.rfind('/', 1) + 1:url.rfind('.')]
print(house_id)