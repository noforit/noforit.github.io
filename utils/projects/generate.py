
import pandas as pd
import time
import codecs

df = pd.read_excel('projects.xlsx')

for i in range(df.shape[0]):
    line = df.loc[i]
    title, code, description, character, date, extra = list(line)
    date = date.strftime("%Y-%m-%d")
    with codecs.open(title + '.md', 'w', encoding='utf-8') as f:
        f.write('---\n')
        if code != '-':
            title = title + '（批准号：' + str(code) + '）'
        f.write(f'title: \"{title}\"\n')
        # f.write(f'code: "{code}"')
        f.write(f'date: \"{date}\"\n')
        f.write(f'sort_by: \"date\"\n')
        f.write(f'description: \"{description}\"\n')
        f.write('extra:\n')
        if extra != '-':
            extras = extra.split('\n')
            for item in extras:
                f.write(f'\t{item}\n')
        f.write('---\n')
        f.write(f'\n#{title}\n')


