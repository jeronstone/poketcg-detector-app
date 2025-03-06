from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import easyocr
reader = easyocr.Reader(['en'])

result = reader.readtext('/home/jestone/tcgdetector/card_imgs_desc/Abomasnow_4_Rare_sm6-4.jpg', detail=0)
result2 = reader.readtext('/home/jestone/tcgdetector/card_imgs_desc/Heracross_8_Uncommon_sv6-8.jpg', detail=0)
result3 = reader.readtext('/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/IMG_5314.jpg', detail=0)
#result = sorted(result, key=lambda x: x[2])
#print(result)
abomasnow = " ".join([word for line in result for word in line.split()])
heracrossreal = " ".join([word for line in result2 for word in line.split()])
heracrosspic = " ".join([word for line in result3 for word in line.split()])

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([abomasnow, heracrossreal, heracrosspic])

similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[2])
similarity_score2 = cosine_similarity(tfidf_matrix[1], tfidf_matrix[2])
print(f"Cosine Similarity: {similarity_score[0][0]:.4f}")
print(f"Cosine Similarity2: {similarity_score2[0][0]:.4f}")