import re
import yaml

# В данном случае {0} - слово, {1} - "небуквенные символы (пробелы, знаки препинания и т.п.)"
match_patterns = ['{0}{1}и{1}{0}', '{0}{1}[аи] также{1}{0}']

dict_file = 'whole_positive.yml'
text_file = 'reviews_lemmatized.txt'
out_file = 'out10.yml'

class ExplicitDumper(yaml.SafeDumper):
    """
    A dumper that will never emit aliases.
    """

    def ignore_aliases(self, data):
        return True

def read_yaml(fn):
    '''
    Читаем исходный словарь
    '''
    ret = None
    with open (fn, "r", encoding='utf-8') as f:
        ret = yaml.load(f)
        f.close()
    return ret

def pattern_search(text, pattern):
    non_ltr = '[^а-яёА-ЯЁ]{1,}'
    adj_pat = '([а-яёА-ЯЁ]*(?:[иоы]й))'
    found = re.findall(str.format(pattern, adj_pat, non_ltr), text)
    return found

def bootstrap (known, pairs):
    add = 0
    for pair in pairs:
        a = pair[0] in known
        b = pair[1] in known
        if a and not b:
            #Строка 1
            #known.append(pair[1])
            known[pair[1]] = known[pair[0]]
            add += 1
        if b and not a:
            # Строка 2
            #known.append(pair[0])
            known[pair[0]] = known[pair[1]]
            add += 1
    return add


# Прочитаем словарь
lemmas = read_yaml(dict_file)

#print(lemmas)

# Выберем все прилагательные (в словаре инфинитивы)
adj = {}
for l in lemmas:
    for w in l.split(' '):
        if w.endswith('ий') or w.endswith('ой') or w.endswith('ый'):
            if not w in adj:
                adj[w] = lemmas[l]

# Прочитаем текст
text = ''
with open (text_file, 'r', encoding='utf-8') as f:
    text = f.read()
    f.close()

pairs = []
for p in match_patterns:
    pairs.extend(pattern_search(text, p))

x = None
print (len(adj))
# Пока алгоритм даёт новые, продолжаем
while x != 0:
    x = bootstrap(adj, pairs)
    print ('+' + str(x) + ': ' + str(len(adj)))
# Вывод в файл
with open(out_file, 'w') as f:
    f.write(yaml.dump(adj, allow_unicode=True, Dumper = ExplicitDumper))
    f.close()

