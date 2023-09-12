import collections
import pathlib

from cldfbench import CLDFSpec
from cldfbench import Dataset as BaseDataset
from clldutils.misc import slug


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "audersetinterrog"

    def cldf_specs(self):
        return CLDFSpec(dir=self.cldf_dir, module="StructureDataset")

    def cmd_makecldf(self, args):

        # read raw data

        parameters = list(self.etc_dir.read_csv("parameters.csv", dicts=True))
        codes_by_id = collections.OrderedDict(
            (row['ID'], row)
            for row in self.etc_dir.read_csv('codes.csv', dicts=True))

        raw_data = list(self.raw_dir.read_csv(
            "InterrogativeRelativeIE_Appendix1.csv", dicts=True))

        # knead into a cldfifiable shape

        languages_by_id = collections.OrderedDict()
        for row in raw_data:
            if row['Glottocode'] not in languages_by_id:
                languages_by_id[row['Glottocode']] = {
                    'ID': row['Glottocode'],
                    'Glottocode': row['Glottocode'],
                    'Name': row['Language'],
                    'Family': row['Branch'],
                    'Subbranch': row['Subbranch'],
                    'Subsubbranch': row['Subsubbranch'],
                    'EarlyTimeBP': row['EarlyTimeBP'],
                    'LateTimeBP': row['LateTimeBP'],
                    'AvTimeBP': row['AvTimeBP'],
                    'Latitude': row['Latitude'],
                    'Longitude': row['Longitude'],
                }

        constructions = [
            {
                'ID': row['ID'],
                'Name': '{} relative pronoun {}'.format(
                    languages_by_id[row['Glottocode']]['Name'],
                    row['RMform']),
                'Language_ID': row['Glottocode'],
            }
            for row in raw_data]

        cvalues = []
        for row in raw_data:
            for parameter in parameters:
                if parameter['ID'] == 'rmform':
                    code_id = None
                    comment = row['Notes']
                else:
                    code_id = '{}-{}'.format(
                        parameter['ID'], slug(row[parameter['Sheet_Column']]))
                    comment = None
                cvalue = {
                    'ID': '{}-{}'.format(row['ID'], parameter['ID']),
                    'Construction_ID': row['ID'],
                    'Parameter_ID': parameter['ID'],
                    'Value': row[parameter['Sheet_Column']],
                    'Code_ID': code_id,
                    'Comment': comment,
                }
                cvalues.append(cvalue)

        parameters.append({
            'ID': 'rmforms',
            'Name': 'RMForms',
            'Description': 'collection of relative markers used in a language',
        })
        forms_by_language = collections.OrderedDict()
        for row in raw_data:
            glottocode = row['Glottocode']
            if glottocode not in forms_by_language:
                forms_by_language[glottocode] = []
            forms_by_language[glottocode].append(row['RMform'])
        values = [
            {
                'ID': 'rmforms-{}'.format(lang_id),
                'Language_ID': lang_id,
                'Parameter_ID': 'rmforms',
                'Value': ' / '.join(forms),
            }
            for lang_id, forms in forms_by_language.items()]

        # cldf output

        args.writer.cldf.add_component(
            "LanguageTable",
            "Family",
            "Subbranch",
            "Subsubbranch",
            "EarlyTimeBP",
            "LateTimeBP",
            "AvTimeBP",
        )
        args.writer.cldf.add_component("ParameterTable")
        args.writer.cldf.add_component("CodeTable")
        args.writer.cldf.add_table(
            'constructions.csv',
            'http://cldf.clld.org/v1.0/terms.rdf#id',
            'http://cldf.clld.org/v1.0/terms.rdf#languageReference',
            'http://cldf.clld.org/v1.0/terms.rdf#name',
            'http://cldf.clld.org/v1.0/terms.rdf#description')
        args.writer.cldf.add_table(
            'cvalues.csv',
            'http://cldf.clld.org/v1.0/terms.rdf#id',
            'Construction_ID',
            'http://cldf.clld.org/v1.0/terms.rdf#parameterReference',
            'http://cldf.clld.org/v1.0/terms.rdf#codeReference',
            'http://cldf.clld.org/v1.0/terms.rdf#value',
            'http://cldf.clld.org/v1.0/terms.rdf#comment')

        args.writer.cldf.add_foreign_key(
            'cvalues.csv', 'Construction_ID',
            'constructions.csv', 'ID')

        args.writer.objects['LanguageTable'] = languages_by_id.values()
        args.writer.objects['constructions.csv'] = constructions
        args.writer.objects['ParameterTable'] = parameters
        args.writer.objects['CodeTable'] = codes_by_id.values()
        args.writer.objects['cvalues.csv'] = cvalues
        args.writer.objects['values.csv'] = values
