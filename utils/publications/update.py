import re
from pathlib import Path
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

mapping = {
    'IEEE transactions on audio speech and language processing': "IEEE/AUDIO/LANGUAGE",
    'Proceedings of the Shared Task on Cross-Framework Meaning Representation Parsing at the 2019 Conference on Natural Language Learning': "MRP",
    'Proceedings of the IJCNLP 2017 Tutorial Abstracts': "IJCNLP",
    'Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing EMNLP': "EMNLP",
    '2017 second international conference on mechanical control and computer engineering ICMCCE': "ICMCCE",
    'NA': "NA",
    'Proceedings of the 2011 Conference on Empirical Methods in Natural Language Processing': "EMNLP",
    'Proceedings of the CoNLL 2017 Shared Task Multilingual Parsing from Raw Text to Universal Dependencies': "CoNLL",
    'Proceedings of the AAAI conference on artificial intelligence': "AAAI",
    'TAC': "TAC",
    'Proceedings of the 29th International Conference on Computational Linguistics': "COLING",
    'IEEE Journal of Biomedical and Health Informatics': "IEEE/BIO/HEALTH",
    'Proceedings of the CoNLL 2018 Shared Task Multilingual Parsing from Raw Text to Universal Dependencies': "CoNLL",
    'ACM Transactions on Asian Language Information Processing TALIP': "ACM/TALIP",
    'Proceedings of COLING 2016 the 26th International Conference on Computational Linguistics Technical Papers': "COLING",
    'Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics Volume 1 Long Papers': "ACL",
    'Citeseer': "Citeseer",
    'Proceedings of the CoNLL 2020 Shared Task Cross-Framework Meaning Representation Parsing': "CoNLL",
    'Proceedings of the AAAI Conference on Artificial Intelligence': "AAAI",
    'Proceedings of the Ninth Conference on Computational Natural Language Learning CoNLL-2005': "CoNLL",
    'BMC bioinformatics': "BMC/BIO",
    'AI Open': "AI Open",
    'Proceedings of the Thirteenth Conference on Computational Natural Language Learning CoNLL 2009 Shared Task': "CoNLL",
    'Proceedings of the Second CIPS-SIGHAN Joint Conference on Chinese Language Processing': "CIPS-SIGHAN",
    'Proceedings of the Third International Joint Conference on Natural Language Processing Volume-II': "IJCNLP",
    'Proceedings of the Twenty-Seventh AAAI Conference on ArtificialIntelligence July 14-18 2013 Bellevue Washington USA': "AAAI",
    'Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing': "EMNLP",
    'Proceedings of the Fourth International Workshop on Semantic Evaluations SemEval-2007': "SemEval",
    'SEM 2012 The First Joint Conference on Lexical and Computational Semantics -- Volume 1 Proceedings of the main conference and the shared task and Volume 2 Proceedings of the Sixth International Workshop on Semantic Evaluation SemEval 2012': "SemEval",
    'Proceedings of the 50th Annual Meeting of the Association for Computational Linguistics Volume 2 Short Papers': "ACL",
    'Notes of the First Workshop on Syntactic Analysis of Non-Canonical Language SANCL': "SANCL",
    'Proceedings of the 2013 Conference of the North American Chapter of the Association for Computational Linguistics Human Language Technologies': "NAACL",
    'IEEEACM transactions on audio speech and language processing': "IEEE/AUDIO/LANGUAGE",
    'Proceedings of the 14th Conference of the European Chapter of the Association for Computational Linguistics': "EACL",
    'Proceedings of the 27th International Conference on Computational Linguistics': "COLING",
    'Proceedings of SEM 2021 The Tenth Joint Conference on Lexical and Computational Semantics': "SemEval",
    '2010 4th International Universal Communication Symposium': "IUCS",
    'Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics Volume 1 Long Papers': "ACL",
    'IEEEACM Transactions on Audio Speech and Language Processing': "IEEE/AUDIO/LANGUAGE",
    'Coling 2010 Demonstrations': "COLING",
    'High technology letters': "High technology letters",
    'Proceedings of the 23rd International Conference on Computational Linguistics Coling 2010': "COLING",
    'Expert Systems with Applications': "Expert Systems with Applications",
    'WWW 20 The Web Conference 2020 Taipei Taiwan April 20-24 2020': "WWW",
    'Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing EMNLP-IJCNLP': "EMNLP",
    'Companion Volume to the Proceedings of Conference including PostersDemos and tutorial abstracts': "COLING",
    'ACM Transactions on Asian and Low-Resource Language Information Processing TALLIP': "ACM/TALLIP",
    'Proceedings of the 3rd Workshop on Natural Language Processing Techniques for Educational Applications NLPTEA2016': "NLPTEA",
    'International conference on advanced data mining and applications': "ICADMA",
    'Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing Volume 1 Long Papers': "ACL",
    'Proceedings of the 5th Workshop on Natural Language Processing Techniques for Educational Applications': "NLPTEA",
    'International Conference on Intelligent Text Processing and Computational Linguistics': "CICLing",
    'Proceedings of the Thirty-Second AAAI Conference on Artificial IntelligenceAAAI-18 the 30th innovative Applications of Artificial IntelligenceIAAI-18 and the 8th AAAI Symposium on Educational Advances inArtificial Intelligence EAAI-18 New Orleans Louisiana USA February2-7 2018': "AAAI",
    'Proceedings of the Thirtieth AAAI Conference on Artificial IntelligenceFebruary 12-17 2016 Phoenix Arizona USA': "AAAI",
    'Findings of the Association for Computational Linguistics EMNLP 2020': "EMNLP(Findings)",
    'Heliyon': "Heliyon",
    'CoNLL 2008 Proceedings of the Twelfth Conference on Computational Natural Language Learning': "CoNLL",
    'IEEEACM Transactions on audio speech and language processing': "IEEE/AUDIO/LANGUAGE",
    'Proceedings of the Twenty-Fifth International Joint Conference onArtificial Intelligence IJCAI 2016 New York NY USA 9-15 July2016': "IJCAI",
    'IEEE Transactions on Knowledge and Data Engineering': "IEEE/Knowledge/Data",
    'Journal of Artificial Intelligence Research': "AI/RESEARCH",
    'Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics': "ACL",
    'Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing': "EMNLP",
    'Proceedings of the 2015 Conference of the North American Chapter of the Association for Computational Linguistics Human Language Technologies': "NAACL",
    'Proceedings of the Twenty-Ninth International Joint Conference onArtificial Intelligence IJCAI 2020': "IJCAI",
    'Workshop on the Syntactic Analysis of Non-Canonical Language SANCL 2012 Montreal Canada': "SANCL(Workshop)",
    'Proceedings of COLING 2012': "COLING",
    'Journal of Chinese information processing': "JCIP",
    'Proceedings of COLING 2014 the 25th International Conference on Computational Linguistics Technical Papers': "COLING",
    'Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing System Demonstrations': "EMNLP(Demo)",
    'Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics': "ACL",
    'Chinese Computational Linguistics and Natural Language Processing Based on Naturally Annotated Big Data': "CCL",
    'ArXiv preprint': "ArXiv",
    'Data Intelligence': "DI",
    'Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics System Demonstrations': "ACL(Demo)",
    '9th IEEE International Conference on Cognitive Informatics ICCI10': "ICCI",
    'Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing Volume 1 Long Papers': "ACL",
    'Proceedings of the Twenty-Seventh International Joint Conference onArtificial Intelligence IJCAI 2018 July 13-19 2018 StockholmSweden': "IJCAI",
    'Proceedings of the 50th Annual Meeting of the Association for Computational Linguistics Volume 1 Long Papers': "ACL",
    'CCF International Conference on Natural Language Processing and Chinese Computing': "NLPCC",
    'Proceedings of the Third SIGHAN Workshop on Chinese Language Processing': "SIGHAN",
    '2012 International Conference on Asian Language Processing': "ICALP",
    'Journal of Chinese Information Processing': "JCIP",
    'The twentieth anniversary Proceedings of the Chinese Information Processing Society of China sequel': "CIPS",
    'Proceedings of the 28th International Conference on Computational Linguistics': "COLING",
    'Proceedings of the 45th Annual Meeting of the Association of Computational Linguistics': "ACL",
    'Proceedings of ACL 2017 System Demonstrations': "ACL(Demo)",
    'The Thirty-Fourth AAAI Conference on Artificial Intelligence AAAI2020 The Thirty-Second Innovative Applications of Artificial IntelligenceConference IAAI 2020 The Tenth AAAI Symposium on EducationalAdvances in Artificial Intelligence EAAI 2020 New York NY USAFebruary 7-12 2020': "AAAI",
    'Proceedings of the 52nd Annual Meeting of the Association for Computational Linguistics Volume 1 Long Papers': "ACL",
    '2010 International Conference on Asian Language Processing': "ICALP",
    'Proceedings of the 5th International Workshop on Semantic Evaluation': "SemEval",
    'Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing EMNLP': "EMNLP",
    'Proceedings of the COLINGACL 2006 Main Conference Poster Sessions': "COLING",
    'International Journal of Machine Learning and Cybernetics': "IJMLC",
    'Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics Human Language Technologies Volume 1 Long Papers': "NAACL",
    'Findings of the Association for Computational Linguistics ACL-IJCNLP 2021': "ACL(Findings)",
    'China Machine Press Beijing': "CMP",
    'Human Language Technologies The 2010 Annual Conference of the North American Chapter of the Association for Computational Linguistics': "NAACL",
    'Proceedings of 5th International Joint Conference on Natural Language Processing': "IJCNLP",
    'Proceedings of Human Language Technologies The 2009 Annual Conference of the North American Chapter of the Association for Computational Linguistics Companion Volume Short Papers': "NAACL",
    'Iscience': "Iscience",
}

author_dict = {
    'Bo Sun': 'Sun Bo',
    'Sun Bo': 'Sun Bo',
    'Zheng Bo': 'Zheng Bo',
    'Bo Zheng': 'Zheng Bo',
    'Zhang Yi': 'Zhang Yi',
    'Yi Zhang': 'Zhang Yi',
    'Ren Bin': 'Ren Bin',
    'Bin Ren': 'Ren Bin',
    'Wang Zhe': 'Wang Zhe',
    'Zhe Wang': 'Wang Zhe',
    'Han Yu': 'Han Yu',
    'Yu Han': 'Han Yu',
    'Che W': 'Che Wanxiang',
    'Che WX': 'Che Wanxiang',
    'Che Wan-xiang': 'Che Wanxiang',
    'CHE Wan-xiang': 'Che Wanxiang',
    'Liu T': 'Liu Ting',
    'Liu Y': 'Liu Yang',
    'Zeyang Lei': 'Lei Zeyang',
    'Aw Ai Ti': 'Aw AiTi',
    'HUANG Yong-guang': 'Huang Yongguang',
}


def clean_file_name(filename: str):
    return re.sub(r'[^a-zA-Z0-9 -]', r'', filename)


def get_data(entry, keys):
    for key in keys:
        if key in entry:
            return entry[key]
    return None


def process_author(author):
    author = author.replace(',', '').strip()
    author = author_dict.get(author, author)
    return author


def main():
    with open('test/all.bib', 'r') as f:
        publishers = set()
        bib_database: BibDatabase = bibtexparser.load(f)

        writer = BibTexWriter()
        for entry in bib_database.entries:
            raw_title = get_data(entry, ['title'])
            raw_title = raw_title.replace('{', '').replace('}', '').replace('\n', '')
            title = clean_file_name(raw_title)

            authors = get_data(entry, ['author'])
            authors = authors.replace('\n', ' ')

            raw_publisher = get_data(entry, ['booktitle', 'journal', 'publisher', 'venue'])
            if raw_publisher is not None:
                publisher = clean_file_name(raw_publisher)
                publisher = mapping.get(publisher, "NA")
            else:
                publisher = None

            url = get_data(entry, ["url", 'eprint_url', 'pub_url'])
            year = get_data(entry, ['year', 'pub_year'])
            bibtex_id = get_data(entry, ['ID'])

            publishers.add((publisher, year))

            date = year + '-01-01'
            filename = year + '-' + title
            filename = clean_file_name(filename)[:128]
            page_num = get_data(entry, ['pages', 'volume'])
            if page_num:
                info = raw_publisher + ', ' + page_num + ', ' + year + '. '
            else:
                info = raw_publisher + ', ' + year + '. '
            extra = [
                f'  title: "{raw_title}"',
                f'  publisher: "{info}"',
                f'  author: "{authors}"',
                f'  bibtex: bibtex/{bibtex_id}.bib',
                f'  year: {year}',
            ]
            if url is not None:
                extra.append(f'  pdf: {url}')
            authors = authors.split('and')
            authors = [process_author(author) for author in authors]
            authors = ", ".join([f"\"{author}\"" for author in authors])
            extra = '\n'.join(extra)
            to_md = f'''---
title: "{title}"
date: {date}
sort_by: "date"
taxonomies:
  authors: [ {authors} ]
  publisher: ["{publisher}"]
  publish_year: ["{year}"]
extra:
{extra}
---
'''

            if publisher is not None and year is not None and year != 'NA':
                publications_dir = Path('test/publications')
                publications_dir.mkdir(exist_ok=True)
                with open(publications_dir / f'{filename}.md', 'w') as f:
                    f.write(to_md)
                bibtex_dir = Path('test/bibtex')
                bibtex_dir.mkdir(exist_ok=True)
                with open(bibtex_dir / f'{bibtex_id}.bib', 'w') as f:
                    db = BibDatabase()
                    db.entries = [entry]
                    f.write(writer.write(db))
            else:
                print(entry)
        # pprint(publishers)


if __name__ == '__main__':
    main()
