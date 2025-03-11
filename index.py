from similarity import Similarity
from api_calls import *
import sys
import time
import os
#from app import get_pickle_data
import cv2
import json
import urllib
import numpy as np

sim = Similarity(imgproc=False)

def get_prediction(imtotest, data, pths, vectorizer, matrix):

    #print('--------------------')
    #print(f'TESTING: {imtotest}')
    st = time.time()

    swt = time.time()

    print('chat1')

    req = urllib.request.urlopen(imtotest)

    print('chat2')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    print('chat3')

    im = cv2.imdecode(arr, -1)

    print(f'chat?')
    # if IMAGE_RECG:
    #     t1 = sim.imageEncoder(im)
    txt = sim.get_text(im)
    v1 = sim.vector_transform(vectorizer, txt)
    print(f'Process input img time: {time.time() - swt}')

    similarities = []
    vectors = []

    # if IMAGE_RECG:
    #     for t in data:
    #         similarities.append(sim.tensor_similarity(t1, t['tensor']))

    swt = time.time()
    vectors.append(sim.vector_cosine_similarity(v1, matrix))
    print(f'Cosine time: {time.time() - swt}')

    #print(f'1 Card processed in {time.time()-st}')

    val = []

    # if IMAGE_RECG:
    #     for i, s in enumerate(similarities):
    #         #print(f'{data[i]['path']}: {s} {vectors[0][0][i]}')
    #         val.append((i, math.sqrt(s**2 + (vectors[0][0][i]*100)**2)))
    # else:
    swt = time.time()
    for i in range(len(vectors[0][0])):
        val.append((i, vectors[0][0][i]*100))

    print(f'Indexing time: {time.time() - swt}')

    #print(val)
    swt = time.time()
    val = max(val, key=lambda x: x[1])
    print(f'Find Max time: {time.time() - swt}')
    #print(pths)
    # for i, v in enumerate(val):
    #     head, tail = os.path.split(data[v[0]]['path'])
    #     print(f'Card: {tail}, Score: {v[1]}')
    splits = get_splits(pths[val[0]])
    score = val[1]
    try:
        price = get_price(pths[val[0]])
    except e:
        price = -99

    ret = {
        "pname": splits[0],
        "set": splits[-1],
        "score": round(score, 2),
        "price": price,
        "imagelink": pths[val[0]][2:],
        "time": time.time()-st
    }
    print(json.dumps(ret))
    return json.dumps(ret)

if __name__ == '__main__':
    get_prediction(sys.argv[1])