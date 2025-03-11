from similarity import Similarity
from generate_tensors import load_tensors, generate_tensors
import cv2
import time
import os
import math
import glob
from api_calls import get_price, get_splits

IMAGE_RECG = False
#generate_tensors(finame='coopertest_svstar', only=2)

data, pths, vectorizer, matrix = load_tensors(finame='coopertest_svstar')

print(len(pths))
exit(0)
#print(vectorizer)
#print(matrix)
sim = Similarity()

search_path = os.path.join('/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/', '*')
files = glob.glob(search_path)

skiplist = ['/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/sizzlipede36_when_she_sizzle_on_my.jpg',
            '/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/golett_87.jpg',
            '/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/pupitarLOLPOOPITAR48.jpg',
            '/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/sneasel_61.jpg',
            '/home/jestone/tcgdetector/PokePhotos-001/ConvertedFiles/marill_64.jpg']

for imtotest in files:

    # if imtotest in skiplist:
    #     continue

    print('--------------------')
    print(f'TESTING: {imtotest}')
    st = time.time()

    im = cv2.imread(imtotest, cv2.IMREAD_UNCHANGED)
    if IMAGE_RECG:
        t1 = sim.imageEncoder(im)
    txt = sim.get_text(im)
    v1 = sim.vector_transform(vectorizer, txt)

    similarities = []
    vectors = []

    if IMAGE_RECG:
        for t in data:
            similarities.append(sim.tensor_similarity(t1, t['tensor']))

    vectors.append(sim.vector_cosine_similarity(v1, matrix))

    print(f'1 Card processed in {time.time()-st}')

    val = []

    if IMAGE_RECG:
        for i, s in enumerate(similarities):
            #print(f'{data[i]['path']}: {s} {vectors[0][0][i]}')
            val.append((i, math.sqrt(s**2 + (vectors[0][0][i]*100)**2)))
    else:
        for i in range(len(vectors[0][0])):
            val.append((i, vectors[0][0][i]*100))

    #print(val)
    val = sorted(val, key=lambda x: x[1])
    #print(pths)
    # for i, v in enumerate(val):
    #     head, tail = os.path.split(data[v[0]]['path'])
    #     print(f'Card: {tail}, Score: {v[1]}')
    print(f'PREDICTED CARD: {get_splits(pths[val[-1][0]])} (score {val[-1][1]})')
    #print(f'This card costs ${get_price(pths[val[-1][0]])}!')
