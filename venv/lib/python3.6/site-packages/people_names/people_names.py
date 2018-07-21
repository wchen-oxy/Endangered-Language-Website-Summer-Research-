# coding: utf-8
import re
import unidecode
from slugify import Slugify
# name_format:
# fml  ==> first middle last
# lfm  ==> last first middle

def normalize_string(u_str):
    return unidecode.unidecode(u_str)

def slugify_string(str):
    my_slugify = Slugify()
    my_slugify.to_lower=True
    return my_slugify(str)

def add_name_parts_to_dict(obj, name_parts):
    obj['first_name'] = name_parts['first_name']
    obj['middle_name'] = name_parts['middle_name']
    obj['last_name'] = name_parts['last_name']
    obj['suffix_name'] = name_parts['suffix_name']
    obj['nominal_name'] = name_parts['nominal_name']
    obj['nickname'] = name_parts['nickname']
    obj['slug_name'] = name_parts['slug_name']

def split_name(name_str, name_format, force_split=False): # force_split - add comma if none and return result for (l, f m)
    if name_str == '':
        return {'first_name': '',
                'middle_name': '',
                'last_name': '',
                'suffix_name': '',
                'nominal_name': '',
                'nickname': '',
                'slug_name': ''
        }

    name_str = normalize_string(name_str)
    name_str = _strip_stakeholder_positions(name_str)
    name_str = _reformat_stakeholder_nominal(name_str)
    name_str = name_str.strip()

    if name_format == 'lfm':
        return _process_last_middle_first(name_str, force_split)
    elif name_format == 'fml':
        return _process_first_middle_last(name_str)
    else:
        return {"err": "invalid name format..."}


def _process_first_middle_last(name_str):
    names = {'original_name': name_str}
    name_str = _first_name(name_str)
    name_str = re.sub(',is$','', name_str)
    name_str = name_str.replace(".", "")
    name_str = name_str.replace("*", "")
    name_str = name_str.replace(",", " ")
    name_str = re.sub('\s+',' ', name_str) # done for things like: john smith , jr <-- extra space before comma


    name_arr = name_str.split(" ")
    # print (name_arr)
    nominal_results = _check_and_remove_nominal(name_arr)
    nickname_results = _check_for_nickname_new(nominal_results['arr'])
    name_arr = nickname_results['arr']
    # print (name_arr)
    suffix_name = get_suffix_name(name_arr)
    # print (name_arr)
    prefix_results = _determine_last_name_prefix(name_arr)
    if prefix_results:
        last_name = prefix_results['last_name']
        name_arr = prefix_results['first_middle'].split(" ")
        first_name = _get_first_element(name_arr)
        middle_name = _get_join_elements(name_arr[1:]) # don't pass first element (first_name)
    else:
        last_name = name_arr[-1]
        first_name = _get_first_element(name_arr[:-1])
        middle_name = _get_join_elements(name_arr[1:-1])

    middle_name, last_name = _check_middle_last_name(middle_name, last_name)

    names = {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name}

    names['nickname'] = nickname_results['nickname']
    names['nominal_name'] = nominal_results['nominal_name']
    names['suffix_name'] = suffix_name
    names['slug_name'] = _slugify_name(names) # don't pass first element (first_name)
    return names

def _process_last_middle_first(name_str, force_split):
    if force_split:
        name_str = _check_for_comma(name_str) # check that there's a comma after last name
    name_str = _strip_remaining_same_chars(name_str, ',')
    name_str = _ensure_space_after_comma(name_str)


    name_str = name_str.replace(".", "")
    name_str = name_str.title() # convert to upper/lowercase



    name_arr = name_str.rsplit(", ", 1)
    if len(name_arr) > 1:
        names = _get_last_middle_first(name_arr)
    else:
        return None
    return names

def _check_for_comma(str):
    str_split = str.split()
    if str_split[0].endswith(','):
        return str
    else:
        return ', '.join(str_split)

def _get_last_middle_first(name_arr):
    names = {}
    names['last_name'] = name_arr[0]
    name_arr = (name_arr[1]).split(" ")
    results = _check_and_remove_nominal(name_arr)
    nominal_results = _check_and_remove_nominal(name_arr)
    nickname_results = _check_for_nickname_new(nominal_results['arr'])
    name_arr = nickname_results['arr']
    names['nickname'] = nickname_results['nickname']
    names['nominal_name'] = nominal_results['nominal_name']
    names['suffix_name'] = get_suffix_name(name_arr)
    names['first_name'] = _get_first_element(name_arr)
    names['middle_name'] = _get_join_elements(name_arr[1:]) # don't pass first element (first_name)

    names['slug_name'] = _slugify_name(names) # don't pass first element (first_name)

    ## done if suffix_name in last name vs end of first/middle
    if names['suffix_name'] == '':
        name_arr = (names['last_name']).split(" ")
        names['suffix_name'] = get_suffix_name(name_arr)
        names['last_name'] = _get_join_elements(name_arr)

    return names

def _slugify_name(name):
    return slugify_string(name['first_name'] + ' ' + name['middle_name'] + ' ' + name['last_name'])

# fix for things like Mr.John smith
def _first_name(name_str):
    name = name_str
    match = re.search(r'^(Mr|Ms|Dr)\.(\S.*)', name_str, re.IGNORECASE)
    if match:
        name = "%s %s" % (match.group(1), match.group(2))
    return name

def _get_first_element(names):
    if len(names) == 0:
        return ''
    return str.rstrip(names[0], '.')


def _get_join_elements(names):
    if len(names) == 0:
        return ''
    if len(names) == 1:
        return str.rstrip(names[0], '.')
        # return names[0]
    else:
        return ' '.join(names)

def _check_for_nickname_new(name):
    full_name = ' '.join(name)
    nickname = _check_nickname(full_name)
    return nickname

# remove trailing characters after first occurance (done for Torkelson, Paul, M - remove 2nd comma)
def _strip_remaining_same_chars(str, char):
    first_comma_idx = str.find(char)
    strip_comma_string = str[first_comma_idx+1:].replace(char, "")
    return str[:first_comma_idx+1] + strip_comma_string

# check if name like last_name,first_name (no space after comma)
def _ensure_space_after_comma(str):
    return re.sub(',(?=\S)', ', ', str)


# TODO: this is the worst... fix this sometime...
def _check_middle_last_name(middle_name, last_name):
    middle_name_arr = middle_name.split(" ")
    if len(middle_name_arr) > 1:
        middle = middle_name_arr[0]
        last = last_name
        for idx, m_name in enumerate(middle_name_arr[1:]):
            if len(m_name) == 1:
                middle = '{} {}'.format(middle, m_name)
            else:
                last = '{} {}'.format(m_name, last)

        middle_name = re.sub('\s+', ' ', middle.strip())
        last_name = re.sub('\s+', ' ', last.strip())

    return [middle_name, last_name]

def _check_nickname(name):
    nickname = ''
    nickname_stripped = name
    match = re.search(r'(.*?)(\(|\")(.*)(\)|\")(.*)', name, re.IGNORECASE)
    if match:
        nickname_stripped = match.group(1) + ' ' + match.group(5)
        nickname_stripped = re.sub('\s+',' ', nickname_stripped.strip())

        nickname = _check_nickname_override(match.group(3))
        nickname = nickname.replace("\'", "")
        nickname = nickname.replace("\"", "")
    return {'nickname': nickname, 'arr': nickname_stripped.split(" ")}

def _determine_last_name_prefix(names_arr):
    full_name = ' '.join(names_arr)
    prefixes = ['del', 'van', 'de', 'st', 'da', 'di', 'la', 'le', 'von', 'della', 'du']
    for prefix in prefixes:
        results = _check_for_last_name_prefix(full_name, prefix)
        if results:
            break;
    return results

def _check_for_last_name_prefix(name_str, prefix_to_check):
    prefix_regex = r"(.*?)\b("+re.escape(prefix_to_check)+r"\b.*)"
    match = re.search(prefix_regex, name_str, re.IGNORECASE)
    if match:
        return {'first_middle': match.group(1).strip(), 'last_name': match.group(2).strip()}
    else:
        return None

def _check_and_remove_nominal(names):
    names_no_post_nominal = []
    nominal_name = ''
    for name in names:
        nominal_name_new = _check_post_nominal(name)
        if nominal_name_new == '':
            names_no_post_nominal.append(name)
        nominal_name = _determine_set_name('nominal', nominal_name, nominal_name_new)

    return {'arr': names_no_post_nominal, 'nominal_name': nominal_name}

def _determine_set_name(name_type, name, name_new):
    if name_type == 'nickname':
        name_new = _check_nickname_override(name_new)

    if name == '':
        return name_new
    else:
        return name

def _check_nickname_override(nickname):
    nickname_lowercase = nickname.lower()
    if 'retd' == nickname_lowercase:
        nickname = ''
    elif 'retired' == nickname_lowercase:
        nickname = ''
    elif 'illinois' == nickname_lowercase:
        nickname = ''
    elif 'uk' == nickname_lowercase:
        nickname = ''
    elif 'president du conseil' == nickname_lowercase:
        nickname = ''

    return nickname

def _strip_stakeholder_positions(name_str):
    name_str = name_str.replace("Vice Chairman and Chairman of Goldman Sachs Asia Pacific", "")
    name_str = name_str.replace("Executive Vice President and Chief Financial Officer", "")
    name_str = name_str.replace("Executive Vice President, General Counsel and Secretary of the Corporation", "")
    name_str = name_str.replace("Executive Vice President and Head of Global Compliance", "")
    name_str = name_str.replace("Executive Vice President, Chief of Staff and Secretary to the Board", "")
    name_str = name_str.replace("Executive Vice President and Global Head of Human Capital Management", "")
    name_str = name_str.replace("President and Chief Operating Officer", "")
    name_str = name_str.replace("Chairman and Chief Executive Officer", "")
    name_str = name_str.replace("President and COO", "")
    name_str = name_str.replace("Lead Director", "")
    name_str = name_str.replace("Vice Chairman", "")

    return name_str.strip()

def _reformat_stakeholder_nominal(name_str):
    name_str = name_str.replace("P. Eng.", "P.Eng.")

    return name_str.strip()

def _check_post_nominal(name):
    lowercase_name = name.lower()
    post_nominal = ''
    if 'mr' == lowercase_name:
        post_nominal = 'Mr'
    elif 'ms' == lowercase_name:
        post_nominal = 'Ms'
    elif 'mrs' == lowercase_name:
        post_nominal = 'Mrs'
    elif 'phd' == lowercase_name:
        post_nominal = 'PhD'
    elif 'mba' == lowercase_name:
        post_nominal = 'MBA'
    elif 'mbs' == lowercase_name:
        post_nominal = 'MBS'
    elif 'bsc' == lowercase_name:
        post_nominal = 'BSc'
    elif re.match(r'^bsc\s?\(.*\)$', name, re.IGNORECASE):
        post_nominal = 'BSc'
    elif 'bcomm' == lowercase_name:
        post_nominal = 'BComm'
    elif 'bsc' == lowercase_name:
        post_nominal = 'BSc'
    elif 'bed' == lowercase_name:
        post_nominal = 'BEd'
    elif 'ceng' == lowercase_name:
        post_nominal = 'CEng'
    elif 'fiei' == lowercase_name:
        post_nominal = 'FIEI'
    elif 'msc' == lowercase_name:
        post_nominal = 'MSc'
    elif re.match(r'^msc\s?\(.*\)$', name, re.IGNORECASE):
        post_nominal = 'BSc'
    elif 'be' == lowercase_name:
        post_nominal = 'BE'
    elif 'ba' == lowercase_name:
        post_nominal = 'BA'
    elif 'bs' == lowercase_name:
        post_nominal = 'BS'
    elif 'ma' == lowercase_name:
        post_nominal = 'MA'
    elif 'bm' == lowercase_name:
        post_nominal = 'BM'
    elif 'bcom' == lowercase_name:
        post_nominal = 'BCom'
    elif 'pgeo' == lowercase_name:
        post_nominal = 'PGeo'
    elif 'bmech' == lowercase_name:
        post_nominal = 'BMech'
    elif 'bch' == lowercase_name:
        post_nominal = 'BCh'
    elif 'peng' == lowercase_name:
        post_nominal = 'PEng'
    elif 'eng' == lowercase_name:
        post_nominal = 'Eng'
    elif 'mbbs' == lowercase_name:
        post_nominal = 'MBBS'
    elif 'dr' == lowercase_name:
        post_nominal = 'Dr'
    elif 'md' == lowercase_name:
        post_nominal = 'MD'
    elif 'nd' == lowercase_name:
        post_nominal = 'ND'
    elif 'jd' == lowercase_name:
        post_nominal = 'JD'
    elif 'pharmd' == lowercase_name:
        post_nominal = 'PharmD'
    elif 'obe' == lowercase_name:
        post_nominal = 'OBE'
    elif 'esq' == lowercase_name:
        post_nominal = 'Esq'
    elif 'esquire' == lowercase_name:
        post_nominal = 'Esq'
    elif 'qc' == lowercase_name:
        post_nominal = 'QC'
    elif 'ca' == lowercase_name:
        post_nominal = 'CA'
    elif 'cpa' == lowercase_name:
        post_nominal = 'CPA'
    elif 'cva' == lowercase_name:
        post_nominal = 'CVA'
    elif 'cfe' == lowercase_name:
        post_nominal = 'CFE'
    elif 'cfa' == lowercase_name:
        post_nominal = 'CFA'
    elif 'cbe' == lowercase_name:
        post_nominal = 'CBE'
    elif 'cga' == lowercase_name:
        post_nominal = 'CGA'
    elif 'gen' == lowercase_name:
        post_nominal = 'Gen'
    elif 'general' == lowercase_name:
        post_nominal = 'Gen'
    elif 'con' == lowercase_name:
        post_nominal = 'Con'
    elif 'colonel' == lowercase_name:
        post_nominal = 'Con'
    elif re.match(r'^Gen\s?\(Retd\)$', name, re.IGNORECASE):
        post_nominal = 'Gen'
    elif 'retd' == lowercase_name:
        post_nominal = 'Retd'
    elif 'retired' == lowercase_name:
        post_nominal = 'Retd'
    elif 'maj' == lowercase_name:
        post_nominal = 'Maj'
    elif 'major' == lowercase_name:
        post_nominal = 'Maj'
    elif 'lt' == lowercase_name:
        post_nominal = 'Lt'
    elif 'lieutenant' == lowercase_name:
        post_nominal = 'Lt'
    elif 'col' == lowercase_name:
        post_nominal = 'Col'
    elif 'colonel' == lowercase_name:
        post_nominal = 'Col'
    elif 'adm' == lowercase_name:
        post_nominal = 'Adm'
    elif 'admiral' == lowercase_name:
        post_nominal = 'Adm'
    elif 'comdr' == lowercase_name:
        post_nominal = 'Comdr'
    elif 'commander' == lowercase_name:
        post_nominal = 'Comdr'
    elif 'usa' == lowercase_name:
        post_nominal = 'USA'
    elif 'usaf' == lowercase_name:
        post_nominal = 'USAF'
    elif 'usmc' == lowercase_name:
        post_nominal = 'USMC'
    elif 'usn' == lowercase_name:
        post_nominal = 'USN'
    elif 'us' == lowercase_name:
        post_nominal = 'us'
    elif 'marine' == lowercase_name:
        post_nominal = 'USMC'
    elif 'corps' == lowercase_name:
        post_nominal = 'USMC'
    elif 'sir' == lowercase_name:
        post_nominal = 'Sir'
    elif 'rev' == lowercase_name:
        post_nominal = 'Rev'
    elif 'reverend' == lowercase_name:
        post_nominal = 'Rev'
    elif 'prof' == lowercase_name:
        post_nominal = 'Prof'
    elif 'professor' == lowercase_name:
        post_nominal = 'Prof'
    elif 'dvm' == lowercase_name:
        post_nominal = 'Dmv'
    elif 'the' == lowercase_name:
        post_nominal = 'the'
    elif 'hon' == lowercase_name:
        post_nominal = 'Hon'
    elif 'honorable' == lowercase_name:
        post_nominal = 'Hon'
    elif 'honourable' == lowercase_name:
        post_nominal = 'Hon'
    elif 'judge' == lowercase_name:
        post_nominal = 'Judge'
    elif 'justice' == lowercase_name:
        post_nominal = 'Justice'
    elif 'amb' == lowercase_name:
        post_nominal = 'Amb'
    elif 'ambassador' == lowercase_name:
        post_nominal = 'Amb'
    elif 'gov' == lowercase_name:
        post_nominal = 'Gov'
    elif 'governor' == lowercase_name:
        post_nominal = 'Gov'
    elif 'sen' == lowercase_name:
        post_nominal = 'Sen'
    elif 'senator' == lowercase_name:
        post_nominal = 'Sen'
    elif 'mst' == lowercase_name:
        post_nominal = 'MST'
    elif 'llb' == lowercase_name:
        post_nominal = 'LLB'
    elif 'arct' == lowercase_name:
        post_nominal = 'ARCT'
    elif 'fcpa' == lowercase_name:
        post_nominal = 'FCPA'
    elif 'frcp' == lowercase_name:
        post_nominal = 'FRCP'
    elif 'fca' == lowercase_name:
        post_nominal = 'fca'
    elif 'mining' == lowercase_name:
        post_nominal = 'Mining'
    elif 'engineering' == lowercase_name:
        post_nominal = 'Engineering'
    elif 'fcca' == lowercase_name:
        post_nominal = 'FCCA'
    elif 'frcp' == lowercase_name:
        post_nominal = 'FRCP'
    elif 'dps' == lowercase_name:
        post_nominal = 'DPS'
    elif 'mbchb' == lowercase_name:
        post_nominal = 'MBChB'
    elif 'facp' == lowercase_name:
        post_nominal = 'FACP'
    elif 'facc' == lowercase_name:
        post_nominal = 'FACC'
    elif 'fscai' == lowercase_name:
        post_nominal = 'FSCAI'
    elif 'adv' == lowercase_name:
        post_nominal = 'Adv'
    elif 'advocate' == lowercase_name:
        post_nominal = 'Adv'
    elif 'lld' == lowercase_name:
        post_nominal = 'LLD'
    elif 'llm' == lowercase_name:
        post_nominal = 'LLM'
    elif 'shri' == lowercase_name:
        post_nominal = 'Shri'
    elif 'mph' == lowercase_name:
        post_nominal = 'MPH'
    elif 'facs' == lowercase_name:
        post_nominal = 'FACS'
    elif 'licoechsg' == lowercase_name:
        post_nominal = 'LIC.OEC.HSG'
    elif 'oec' == lowercase_name:
        post_nominal = 'OEC'
    elif 'hsg' == lowercase_name:
        post_nominal = 'HSG'
    elif 'mrcp' == lowercase_name:
        post_nominal = 'MRCP'
    elif 'icdd' == lowercase_name:
        post_nominal = 'ICDD'
    elif 'chrp' == lowercase_name:
        post_nominal = 'CHRP'
    elif 'cma' == lowercase_name:
        post_nominal = 'CMA'

    return post_nominal

def get_suffix_name(names):
    last_element_lower = names[-1].lower()

    if 'jr' == last_element_lower:
        del names[-1]
        suffix_name = 'Jr'
    elif 'sr' == last_element_lower:
        del names[-1]
        suffix_name = 'Sr'
    elif 'ii' == last_element_lower:
        del names[-1]
        suffix_name = 'II'
    elif 'iii' == last_element_lower:
        del names[-1]
        suffix_name = 'III'
    elif 'iv' == last_element_lower:
        del names[-1]
        suffix_name = 'IV'
    elif 'v' == last_element_lower:
        del names[-1]
        suffix_name = 'V'
    elif 'vi' == last_element_lower:
        del names[-1]
        suffix_name = 'VI'
    elif 'vii' == last_element_lower:
        del names[-1]
        suffix_name = 'VII'
    elif 'viii' == last_element_lower:
        del names[-1]
        suffix_name = 'VIII'
    else:
        suffix_name = ''

    if len(names) != 0:
        names[-1] = str.rstrip(names[-1], ',') # strip trailing comma if any from last name
    return suffix_name
