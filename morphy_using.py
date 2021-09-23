import pymorphy2 as pmr
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker
import copy

def name_change(name):

    morph = pmr.MorphAnalyzer(lang='ru')
    maker = PetrovichDeclinationMaker()
    full_name = name.split()
    print(name, full_name)
    f_name = ''
    s_name = ''
    m_name = ''
    full_name_change = copy.deepcopy(full_name)
    for elem in full_name_change:
        is_name = any('Name' in p.tag for p in morph.parse(elem))
        if is_name:
            f_name = elem
            full_name_change.remove(elem)
            break
    for elem in full_name_change:
        is_name = any('Surn' in p.tag for p in morph.parse(elem))
        if is_name:
            s_name = elem
            full_name_change.remove(elem)
            break
    for elem in full_name_change:
        is_name = any('Patr' in p.tag for p in morph.parse(elem))
        if is_name:
            m_name = elem
            full_name_change.remove(elem)
            break

    if len(full_name_change) != 0:
        full_name_change = ""
        for elem in full_name:
            if 'masc' in morph.parse(elem)[0].tag:
                gender = Gender.MALE
            else:
                gender = Gender.FEMALE
            is_name = any('Name' in p.tag for p in morph.parse(elem))
            is_mname = any('Patr' in p.tag for p in morph.parse(elem))
            is_sname = any('Surn' in p.tag for p in morph.parse(elem))
            if is_sname:
                cased_last_name = maker.make(NamePart.LASTNAME, gender, Case.DATIVE, elem)
                full_name_change += ' ' + cased_last_name
            elif is_name:
                cased_name = maker.make(NamePart.FIRSTNAME,gender, Case.DATIVE, elem)
                full_name_change += ' ' + cased_name
            elif is_mname:
                cased_middle_name = maker.make(NamePart.MIDDLENAME, gender, Case.DATIVE, elem)
                full_name_change += ' ' + cased_middle_name
        full_name_change = full_name_change.strip()
        print("Итог: ", full_name_change)
    else:
        if 'masc' in morph.parse(f_name)[0].tag:
            gender = Gender.MALE
        else:
            gender = Gender.FEMALE

        cased_last_name = maker.make(NamePart.LASTNAME, gender, Case.DATIVE, s_name)
        cased_name = maker.make(NamePart.FIRSTNAME,gender, Case.DATIVE, f_name)
        cased_middle_name = maker.make(NamePart.MIDDLENAME, gender, Case.DATIVE, m_name)
        print("Итог: ", (cased_last_name + ' ' + cased_name + ' ' + cased_middle_name).strip())


    
    

'''
    f_name = ''
    print()
    print(morph.parse(name))
    for elem in morph.parse(name):
        print(elem)
        if 'Patr' in elem.tag:
            f_name = elem
    print()

    is_name = any('Patr' in p.tag for p in morph.parse(name))
    print(is_name)
    print("Ok")
'''

'''
    if 'masc' in morph.parse(full_name[1])[0].tag:
        gender = Gender.MALE
    else:
        gender = Gender.FEMALE
    
    if 'masc' in morph.parse(full_name[1])[0].tag:
        cased_last_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.DATIVE, full_name[0])
        cased_name = maker.make(NamePart.FIRSTNAME, Gender.MALE, Case.DATIVE, full_name[1])
    elif 'femn' in morph.parse(full_name[1])[0].tag:
        cased_last_name = maker.make(NamePart.LASTNAME, Gender.FEMALE, Case.DATIVE, full_name[0])
        cased_name = maker.make(NamePart.FIRSTNAME, Gender.FEMALE, Case.DATIVE, full_name[1])
    try:
        if 'masc' in morph.parse(full_name[1])[0].tag:
            cased_middle_name = maker.make(NamePart.MIDDLENAME, Gender.MALE, Case.DATIVE, full_name[2])
            print("Hi", cased_middle_name)
        elif 'femn' in morph.parse(full_name[1])[0].tag:
            cased_middle_name = maker.make(NamePart.MIDDLENAME, Gender.FEMALE, Case.DATIVE, full_name[2])

        return [cased_last_name, cased_name, cased_middle_name]
    except IndexError:
        return [cased_last_name, cased_name, '']
'''