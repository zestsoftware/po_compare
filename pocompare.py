import os, sys

import polib

if len(sys.argv) < 3:
    print "Usage: locales_dir_1 locales_dir_2"
    sys.exit(0)

prod1 = sys.argv[1]
prod2 = sys.argv[2]


def find_po_file(locale_dir, lang):
    for f in os.listdir(locale_dir + '/' + lang + '/LC_MESSAGES'):
        if f.endswith('.po'):
            return locale_dir + '/' + lang + '/LC_MESSAGES/' + f
    
def find_languages(locale_dir):
    languages = []
    for f in os.listdir(locale_dir):
        if os.path.isdir(locale_dir + '/' + f):
            languages.append(f)

    return languages

# We use english as a default languages to find all translations.
en_file_1 = find_po_file(prod1, 'en')
en_file_2 = find_po_file(prod2, 'en')

if not en_file_1:
    print "Missing english po file for first product"
    sys.exit(0)

if not en_file_2:
    print "Missing english po file for second product"
    sys.exit(0)

en_po_1 = polib.pofile(en_file_1)
en_po_2 = polib.pofile(en_file_2)

# We build list of keys.
keys_1 = [entry.msgid for entry in en_po_1]
keys_2 = [entry.msgid for entry in en_po_2]

# We find the ones in common between the two products
common_keys = []
for key in keys_1:
    if key in keys_2:
        common_keys.append(key)

if not common_keys:
    print "No common messages between the two products"
    sys.exit(0)

# Now we find the list of languages defined for each
# product.
prod1_languages = find_languages(prod1)
prod2_languages = find_languages(prod2)

common_languages = []
for lang in prod1_languages:
    if lang in prod2_languages:
        common_languages.append(lang)

if not common_languages:
    print "No common languages between the two products"
    sys.exit(0)

# Now we build a dictionnary for each common message.
# Dictionnary looks like this:
# {msgid1: {lang: {prod1: blabla,
#                  prod2: blibli},
#           lang2: {...}},
#  msgid2: ...}
result = {}

for key in common_keys:
    result[key] = {}

    for lang in common_languages:
        result[key][lang] = {}

        po1 = polib.pofile(find_po_file(prod1, lang))
        po2 = polib.pofile(find_po_file(prod2, lang))

        result[key][lang][prod1] = po1.find(key).msgstr
        result[key][lang][prod2] = po2.find(key).msgstr

for key in result:
    print key
    print '=============================='

    for lang in result[key]:
        print ''
        print 'Translations in ' + lang
        print '----------------------------'

        for prod in result[key][lang]:
            print prod
            print result[key][lang][prod]
