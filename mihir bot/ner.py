import spacy

nlp = spacy.load("en_core_web_sm/en_core_web_sm-3.7.1")

text = "The weather forecast predicts rain in the evening."
doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")