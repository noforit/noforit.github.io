import csv
import os
import shutil

with open('utils/people/people.csv', 'r') as f:
    people = csv.DictReader(f)

    for person in people:
        name = person['\ufeff姓名']
        if person['毕业信息'] == "在读":
            role = person['毕业信息'] + person['在读成员类型']
            date = person['入学年份']
            title = date + "级" + person['在读成员类型']
        else:
            role = person['毕业信息'] + person['毕业成员类型']
            date = person['毕业年份'] if not '年' in person['毕业年份'] else person['毕业年份'][:-1]
            title = date + "届" + person['毕业成员类型']

        info = f'''---
title: "{name}"
date: {date}-02-10
sort_by: "date"
extra:
  role: "Faculty"
  title: "{title}"
  year: "{date}"
  name: "{name}"
  mail: ""
  homepage: "{person['个人主页']}"
  image: "{'/images/photo/' + name + "." + person['照片'].split('.')[-1]}"
---
'''
        with open('./content/people/{}/{}.md'.format(role, name), 'w') as p:
            p.write(info)

for image in os.listdir("static/images/photo"):
    name, suffix = image.split('.')
    if name.count('-') > 1:
        _, name, nth, *args = name.split('-')
        if len(args) == 5:
            new_name = '-'.join([name, nth]) + '.' + suffix
        else:
            new_name = name + '.' + suffix
        shutil.move(f"static/images/photo/{image}", f"static/images/photo/{new_name}")
        # print(len(args), f"static/images/photo/{image}", f"static/images/photo/{new_name}")
