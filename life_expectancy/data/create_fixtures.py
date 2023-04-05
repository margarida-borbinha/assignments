from life_expectancy.cleaning import clean_data, load_data

data = load_data("./eu_life_expectancy_raw.tsv")
data = data.sample(1000)
data.to_csv("./eu_life_expectancy_sample.tsv", sep="\t", index=None)

data = clean_data(data, "PT")
data.to_csv("../tests/fixtures/pt_life_expectancy_expected.csv", index=None)
