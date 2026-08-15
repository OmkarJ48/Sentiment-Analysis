from textblob import TextBlob
text = input("Enter your statement - ");
blob = TextBlob(text)
polarity = blob.sentiment.polarity
subjectivity=blob.sentiment.subjectivity
print("")
print("Sentence - ",text)
print("")
print("Polarity - ",polarity)
print("Subjectivity - ",subjectivity)
