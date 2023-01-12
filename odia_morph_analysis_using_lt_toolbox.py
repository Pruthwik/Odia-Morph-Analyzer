"""Convert ."""
import os
from argparse import ArgumentParser
from re import search
from wxconv import WXC
from re import findall
from re import finditer


# Odia vowels
odia_vowels = ['a', 'A', 'i', 'I', 'e', 'E', 'o', 'O']
# wx->utf and utf->wx converters for Odia
conv_u2w = WXC(order='utf2wx', lang='ori')
conv_w2u = WXC(order='wx2utf', lang='ori')
odia_numbers = '[\U00000B66-\U00000B6F]+'
english_numbers = '[0-9]+'
plural_vibhakti_markers = ['mAnafku', 'mAnafkare', 'mAnafkara', 'mAnafkaTAre', 'mAnafkaru', 'gudiku', 'gudikara', 'gudikaru', 'gudikaTAre', 'gudikare', 'gudZiku', 'gudZikara', 'gudZikaru', 'gudZikaTAre', 'gudZikare', 'gudZAku', 'gudZAkara', 'gudZAkaru', 'gudZAkaTAre', 'gudZAkare', 'gudAku', 'gudAkara', 'gudAkaru', 'gudAkaTAre', 'gudAkare']
plural_vibhakti_markers_at_end = '|'.join([plural_vibhakti_marker + '$' for plural_vibhakti_marker in plural_vibhakti_markers])
plural_direct_markers = ['mAne', 'gudA', 'gudZA', 'gudZAka', 'gudZika', 'gudika']
plural_direct_markers_at_end = '|'.join([plural_direct_marker + '$' for plural_direct_marker in plural_direct_markers])
singular_vibhakti_markers = ['re', 'ra', 'ru', 'TAre', 'TAru', 'fku', 'fka', 'fkara', 'fkaTAru', 'fkaTAre', 'ku', 'xbArA', 'fkaxbArA']
singular_vibhakti_markers_at_end = '|'.join([singular_vibhakti_marker + '$' for singular_vibhakti_marker in singular_vibhakti_markers])


def map_bis_to_lcat(bis_tag):
    """Convert BIS tag to lcat tag."""
    if search('N\_NN.*', bis_tag):
        return 'n'
    elif bis_tag == 'N_NST':
        return 'nst'
    elif search('^PR\_|^DM\_', bis_tag):
        return 'pn'
    elif search('^V\_', bis_tag):
        return 'v'
    elif search('^RP\_|^CC\_', bis_tag):
        return 'avy'
    elif bis_tag == 'RB':
        return 'adv'
    elif bis_tag == 'JJ':
        return 'adj'
    elif bis_tag == 'PSP':
        return 'psp'
    elif bis_tag in ['RD_PUNC', 'RD_SYM']:
        return 'punc'
    elif bis_tag in ['RD_RDF', 'RD_UNK', 'RD_BUL']:
        return 'unk'
    elif bis_tag in ['QT_QTC', 'QT_QTO']:
        return 'num'
    elif bis_tag in ['QT_QTF', 'RD_ECH']:
        return 'avy'


def read_lines_from_file_with_blanks(file_path):
    """Read lines from a file without blanks."""
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.readlines()


def read_lines_from_file_without_blanks(file_path):
    """Read lines from a file without blanks."""
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return [line.strip() for line in file_read.readlines() if line.strip()]


def write_lines_to_file(lines, file_path):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines) + '\n')


def convert_lexical_category_into_af_form(feature_value):
    """Convert lexical category (lcat) into an acceptable af form in SSF."""
    if feature_value in ['conj', 'neg', 'emph']:
        return 'avy'
    elif feature_value == 'prsg':
        return 'psp'
    elif feature_value == 'p':
        return 'pn'
    else:
        return feature_value


def convert_number_into_af_form(feature_value):
    """Convert number feature into an acceptable af form in SSF."""
    if feature_value == 's':
        return 'sg'
    elif feature_value == 'p':
        return 'pl'
    else:
        return feature_value


def convert_person_into_af_form(feature_value):
    """Convert person into an acceptable af form in SSF."""
    if feature_value == 'u':
        return '1'
    elif feature_value == 'a':
        return '3'
    elif feature_value in ['m', 'm_h0']:
        return '2'
    elif feature_value in ['m_h1', 'm_h2']:
        return '2h'
    else:
        return feature_value


def find_morph_for_missing_word(token, token_wx, pos, lcat, next_token):
    """Find morph for missing word."""
    if pos in ['N_NN', 'N_NNP', 'V_VM_VNF', 'V_VM_VNF']:
        found_vibhakti_plural = search(plural_vibhakti_markers_at_end, token_wx)
        if found_vibhakti_plural:
            case = 'o'
            gender = 'any'
            number = 'pl'
            person = '3'
            found_vibhakti_singular = search(singular_vibhakti_markers_at_end, token_wx)
            if found_vibhakti_singular:
                suff = found_vibhakti_singular.group(0)
                tam = conv_w2u.convert(suff)
                root_wx = token_wx[: len(token_wx) - len(suff)]
                root_utf = conv_w2u.convert(root_wx)
        else:
            found_vibhakti_singular = search(singular_vibhakti_markers_at_end, token_wx)
            if found_vibhakti_singular:
                suff = found_vibhakti_singular.group(0)
                tam = conv_w2u.convert(suff)
                root_wx = token_wx[: len(token_wx) - len(suff)]
                root_utf = conv_w2u.convert(root_wx)
                case = 'o'
                if lcat == 'n':
                    gender = 'any'
                    number = 'sg'
                    person = '3'
                else:
                    gender = 'any'
                    number = 'any'
                    person = 'any'
            else:
                found_plural_direct = search(plural_direct_markers_at_end, token_wx)
                if found_plural_direct:
                    suff = '0'
                    tam = '0'
                    plural_direct_ind = found_plural_direct.group(0)
                    root_wx = token_wx[: len(token_wx) - len(plural_direct_ind)]
                    root_utf = conv_w2u.convert(root_wx)
                    case = 'd'
                    gender = 'any'
                    number = 'pl'
                    person = '3'
                else:
                    root_utf = token
                    root_wx = token_wx
                    gender, number, person = 'any', 'any', 'any'
                    if next_token in ['ସହିତ', 'ଦ୍ଵାରା', 'ଠାରେ', 'ପାଇଁ']:
                        case = 'o'
                    else:
                        if lcat == 'n':
                            case = 'd'
                            tam, suff = '0', '0'
                        elif lcat == 'v':
                            case = ''
                            tam, suff = '0', '0'
                        else:
                            case = ''
                            tam, suff = '', ''
    else:
        root_utf = token
        root_wx = token_wx
        gender, number, person = '', '', ''
        if next_token in ['ସହିତ', 'ଦ୍ଵାରା', 'ଠାରେ', 'ପାଇଁ']:
            case = 'o'
        else:
            case = ''
        tam, suff = '', ''
    if root_wx[-1] not in odia_vowels:
        root_wx = root_wx + 'a'
        root_utf = conv_w2u.convert(root_wx)
    token_morph = "fs af='" + ','.join([root_utf, lcat, gender, number, person, case, tam, suff]) + "'>"
    return token_morph


def run_lt_toolbox_and_convert_into_appropriate_form(lines, morph_dict_path, chunk_flag=0):
    """Run LTTOOLBOX and convert the result into appropriate form."""
    if chunk_flag:
        pattern = '^\d+\.\d+\t'
    else:
        pattern = '^\d+\t'
    updated_lines = []
    for index, line in enumerate(lines):
        line = line.strip()
        if search(pattern, line):
            token_morph = ''
            addr, token, pos = line.strip().split('\t')
            lcat = map_bis_to_lcat(pos)
            token_wx = conv_u2w.convert(token)
            if token not in [',', '/'] and pos in ['RD_SYM', 'RD_PUNC']:
                if token == '।':
                    pos = 'RD_PUNC'
                token_morph = "<fs af='" + token + ",punc,,,,,,'>"
            elif token == ',':
                pos = 'RD_PUNC'
                token_morph = "<fs af='COMMA,punc,,,,,,'>"
            elif token == '/':
                pos = 'RD_SYM'
                token_morph = "<fs af='BACKSLASH,punc,,,,,,'>"
            elif search(english_numbers + '|' + odia_numbers, token) or pos in ['QT_QTC', 'QT_QTO']:
                token_morph = token_morph = "<fs af='" + token + ",num,,,,,,'>"
            else:
                os.system("echo " + token_wx + " | lt-proc " + morph_dict_path + " > temp.txt")
                token_morph = read_lines_from_file_without_blanks("temp.txt")[0]
                os.system("rm -rf temp.txt")
                if not findall('<.*?>', token_morph):
                    token_morph = ''
                else:
                    morphs = list(finditer('/', token_morph))
                    fs_lists = []
                    if len(morphs) == 1:
                        token_morph_in_non_af_form = [token_morph[morphs[0].end():]]
                    else:
                        token_morph_in_non_af_form = []
                        for morph, next_morph in zip(morphs, morphs[1:]):
                            token_morph_in_non_af_form.append(token_morph[morph.end(): next_morph.start()])
                        token_morph_in_non_af_form.append(token_morph[morphs[-1].end(): -1])
                    for token_info in token_morph_in_non_af_form:
                        root_wx = token_info[: token_info.find('<')]
                        if root_wx[-1] not in odia_vowels:
                            root_wx = root_wx + 'a'
                            root = conv_w2u.convert(root_wx)
                        else:
                            root = conv_w2u.convert(root_wx)
                        lcat_info = search('\<cat\:(.*?)\>', token_info)
                        if lcat_info:
                            lcat_info = lcat_info.group(1)
                            lcat_info = convert_lexical_category_into_af_form(lcat_info)
                        else:
                            lcat_info = ''
                        if lcat_info and lcat != lcat_info:
                            lcat = lcat_info
                        gender = search('\<gen\:(.*?)\>', token_info)
                        if gender:
                            gender = gender.group(1)
                        else:
                            gender = ''
                        number_non_af = search('\<num\:(.*?)\>', token_info)
                        if number_non_af:
                            number_af = convert_number_into_af_form(number_non_af.group(1))
                        else:
                            number_af = ''
                        person_non_af = search('\<per\:(.*?)\>', token_info)
                        if person_non_af:
                            person_af = convert_person_into_af_form(person_non_af.group(1))
                        else:
                            person_af = ''
                        number_non_af = search('\<num\:(.*?)\>', token_info)
                        if number_non_af:
                            number_af = convert_number_into_af_form(number_non_af.group(1))
                        else:
                            number_af = ''
                        case_non_af = search('\<case\:(.*?)\>', token_info)
                        if case_non_af:
                            case_af = case_non_af.group(1)
                        else:
                            case_af = ''
                        if lcat == 'n':
                            tam = search('\<prsg\:(.*?)\>', token_info)
                            if not tam:
                                tam = ''
                            else:
                                tam = tam.group(1)
                                det = search('\<det\:(.*?)\>', token_info)
                                if det:
                                    det = det.group(1)
                                    if det == '0':
                                        pass
                                    else:
                                        tam = tam + '_' + det
                        elif lcat == 'v':
                            tam = search('\<tam\:(.*?)\>', token_info)
                            if not tam:
                                tam = ''
                            else:
                                tam = tam.group(1)
                        else:
                            tam = ''
                        tam_utf = conv_w2u.convert(tam)
                        fs_morph = ','.join([root, lcat, gender, number_af, person_af, case_af, tam_utf, tam])
                        neg = search('\<neg\:(.*?)\>', token_info)
                        if neg:
                            neg_val = neg.group(1)
                            fs_value = "<fs af='" + fs_morph + "' " + "neg='" + neg_val + "'>"
                        else:
                            fs_value = "<fs af='" + fs_morph + "'>"
                        fs_lists.append(fs_value)
                    token_morph = '|'.join(fs_lists)
            if not token_morph:
                print(index + 1, len(lines), lines[index + 1])
                if index < len(lines) - 1 and search(pattern, lines[index + 1]):
                    next_token = lines[index + 1].split('\t')[2]
                else:
                    next_token = ''
                token_morph = find_morph_for_missing_word(token, token_wx, pos, lcat, next_token)
            updated_line = '\t'.join([addr, token, pos, token_morph])
            updated_lines.append(updated_line)
        else:
            if line == '))':
                updated_lines.append('\t' + line)
            else:
                updated_lines.append(line)
    return updated_lines


def main():
    """Pass arguments and call functions here."""
    parser = ArgumentParser()
    parser.add_argument(
        '--input', dest='inp', help="enter the input file path")
    parser.add_argument(
        '--output', dest='out', help="enter the output file path")
    parser.add_argument(
        '--dict', dest='dict', help="enter the morph dict path")
    parser.add_argument(
        '--chunk', dest='chunk', help="enter the chunk flag either 0 or 1", type=int, choices=[0, 1], default=0)
    args = parser.parse_args()
    if not os.path.isdir(args.inp):
        input_lines = read_lines_from_file_with_blanks(args.inp)
        updated_lines = run_lt_toolbox_and_convert_into_appropriate_form(input_lines, args.dict, args.chunk)
        write_lines_to_file(updated_lines, args.out)
    else:
        if not os.path.isdir(args.out):
            os.makedirs(args.out)
        for root, dirs, files in os.walk(args.inp):
            for fl in files:
                input_path = os.path.join(root, fl)
                input_lines = read_lines_from_file_with_blanks(input_path)
                updated_lines = run_lt_toolbox_and_convert_into_appropriate_form(input_lines, args.dict, args.chunk)
                if '.txt' not in fl:
                    file_name = fl + '_mor'
                else:
                    file_name = fl[: fl.find('.txt')] + '_mor.txt'
                output_path = os.path.join(args.out, file_name)
                write_lines_to_file(updated_lines, output_path)


if __name__ == '__main__':
    main()
