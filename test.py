def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_extent(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 99
    assert len(list(cldf_dataset["ParameterTable"])) == 9
    assert len(list(cldf_dataset["CodeTable"])) == 43
    assert len(list(cldf_dataset["ValueTable"])) == 99
    assert len(list(cldf_dataset["cvalues.csv"])) == 1200
