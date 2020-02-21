import collections
import operator
import pathlib

from cldfbench import CLDFSpec
from cldfbench import Dataset as BaseDataset

from clldutils.misc import slug

# TODO: Link to Appendix PDF for description

PARAMETERS = {
    "NCases": "number of case forms (values 0-7)",
    "NClass": "number of gender or inflectional classes (values 0-3)",
    "NNumber": "number of number distinctions (values 0-3)",
    "INT": "is the relative marker also used as an interrogative? - values: yes, related, relatedmaybe, no, NA",
    "Origin": "what is the source of the marker in PIE?",
    "COMP": "is the relative marker also used as a complementizer? - values: yes, no, NA",
    "Genre": "is the form used in spoken or written language? - values: spoken, written, both",
}

CODES = {
    "NCases": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "NA"],
    "NClass": ["0", "1", "2", "3", "NA"],
    "NNumber": ["0", "1", "2", "3", "NA"],
    "INT": ["yes", "related", "relatedmaybe", "no", "NA"],
    "Origin": [
        "KW or L",
        "KW",
        "KW+YO",
        "NA",
        "YO",
        "TO",
        "ONE",
        "KW+TO",
        "YO+KW",
        "TO+KW",
        "L",
        "TO+YO",
    ],
    "COMP": ["yes", "no", "NA"],
    "Genre": ["spoken", "written", "both"],
}


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "audersetinterrog"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module="StructureDataset")

    def cmd_makecldf(self, args):
        args.writer.cldf.add_component(
            "LanguageTable",
            "Branch",
            "Subbranch",
            "Subsubbranch",
            "EarlyTimeBP",
            "LateTimeBP",
            "AvTimeBP",
        )
        args.writer.cldf.add_component("ParameterTable")
        args.writer.cldf.add_component("CodeTable")
        args.writer.cldf.add_component("ExampleTable")

        lines_by_id = collections.OrderedDict(
            [
                (line["ID"], line)
                for line in self.raw_dir.read_csv(
                    "InterrogativeRelativeIE_Appendix1.csv", dicts=True
                )
            ]
        )

        for lang in lines_by_id.values():
            if (
                not lang["Glottocode"]
                in map(operator.itemgetter("ID"), args.writer.objects["LanguageTable"])
                and lang["Glottocode"] != "medgreek"  # TODO: Ask Sandra medgreek
            ):
                args.writer.objects["LanguageTable"].append(
                    dict(
                        ID=lang["Glottocode"],
                        Glottocode=lang["Glottocode"],
                        Name=lang["Language"],
                        Branch=lang["Branch"],
                        Subbranch=lang["Subbranch"],
                        Subsubbranch=lang["Subsubbranch"],
                        EarlyTimeBP=lang["EarlyTimeBP"],
                        LateTimeBP=lang["LateTimeBP"],
                        AvTimeBP=lang["AvTimeBP"],
                        Latitude=lang["Latitude"],
                        Longitude=lang["Longitude"],
                    )
                )

        for parameter, description in PARAMETERS.items():
            args.writer.objects["ParameterTable"].append(
                dict(ID=slug(parameter), Name=parameter, Description=description)
            )

        for code, values in CODES.items():
            for value in values:
                args.writer.objects["CodeTable"].append(
                    dict(
                        ID="{0}-{1}".format(slug(code), slug(value)),
                        Parameter_ID=slug(code),
                        Name=value,
                    )
                )

        for example in lines_by_id.values():
            if example["Glottocode"] != "medgreek":  # TODO: Ask Sandra medgreek
                args.writer.objects["ExampleTable"].append(
                    dict(
                        ID=example["ID"],
                        Language_ID=example["Glottocode"],
                        Primary_Text=example["RMform"],
                    )
                )

        for value in lines_by_id.values():
            for parameter in PARAMETERS.keys():
                if value["Glottocode"] != "medgreek":
                    args.writer.objects["ValueTable"].append(
                        dict(
                            ID="{0}-{1}-{2}".format(
                                value["Glottocode"], slug(parameter), value["ID"]
                            ),
                            Language_ID=value["Glottocode"],
                            Parameter_ID=slug(parameter),
                            Value=value[parameter],
                            Code_ID="{0}-{1}".format(slug(parameter), slug(value[parameter])),
                        )
                    )
