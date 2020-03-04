import collections
import operator
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
        parameters = self.etc_dir.read_csv("parameters.csv", dicts=True)
        codes = self.etc_dir.read_csv("codes.csv", dicts=True)

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
            if not lang["Glottocode"] in map(
                operator.itemgetter("ID"), args.writer.objects["LanguageTable"]
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

        for parameter in parameters:
            args.writer.objects["ParameterTable"].append(
                dict(
                    ID=parameter["ID"], Name=parameter["Name"], Description=parameter["Description"]
                )
            )

        for code in codes:
            args.writer.objects["CodeTable"].append(
                dict(ID=code["ID"], Parameter_ID=code["Parameter_ID"], Name=code["Name"])
            )

        for example in lines_by_id.values():
            args.writer.objects["ExampleTable"].append(
                dict(
                    ID=example["ID"],
                    Language_ID=example["Glottocode"],
                    Primary_Text=example["RMform"],
                )
            )

        for value in lines_by_id.values():
            for parameter in parameters:
                args.writer.objects["ValueTable"].append(
                    dict(
                        ID="{0}-{1}-{2}".format(value["Glottocode"], parameter["ID"], value["ID"]),
                        Language_ID=value["Glottocode"],
                        Parameter_ID=parameter["ID"],
                        Value=value[parameter["Name"]],
                        Code_ID="{0}-{1}".format(parameter["ID"], slug(value[parameter["Name"]])),
                    )
                )
