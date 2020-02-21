def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_extent(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 98
    assert len(list(cldf_dataset["ParameterTable"])) == 7
