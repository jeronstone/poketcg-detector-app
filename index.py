from similarity import Similarity
from generate_tensors import load_tensors

sim = Similarity(imgproc=False)

def get_prediction(imtotest):
    data, vectorizer, matrix = load_tensors(finame='coopertest_sv6')

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
    print(f'PREDICTED CARD: {pths[val[-1][0]]} (score {val[-1][1]})')
    print(f'This card costs ${get_price(pths[val[-1][0]])}!')
