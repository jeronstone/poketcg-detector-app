import dill as pickle
import glob
import os
from similarity import Similarity
import cv2
import time

def generate_tensors(finame='yayayay', only=0):

    wow = time.time()

    sim = Similarity()

    search_path = os.path.join('./card_imgs_desc/', '*sv6*')
    files = glob.glob(search_path)

    # for i, f in enumerate(files):
    #     print(f'{i}: {f}')

    cardtext = []

    if only == 0 or only == 1:
        f = open('tensors_'+finame, "ab")
        #pickle.dump(len(files) , f) 
        for x in files:
            #st = time.time()
            print(f'Generating for {x}')
            im = cv2.imread(x, cv2.IMREAD_UNCHANGED)
            d = sim.imageEncoder(im)
            data = {'tensor': d, 'path': x}#, 'text_vector': v}
            #print(data)
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            cardtext.append(sim.get_text(im))
            #print(f'Encode Time: {time.time() - st}')

    if only == 0 or only == 2:

        paths = []

        if only == 2:
            for x in files:
                print(f'Generating text for {x}')
                im = cv2.imread(x, cv2.IMREAD_UNCHANGED)
                cardtext.append(sim.get_text(im))
                paths.append(x)

        print(f'!{time.time() - wow} read text time gang squad')

        #print(cardtext)
        vectorizer, tfidf_matrix = sim.vectorize_text(cardtext)
        #print(vectorizer)
        #print(tfidf_matrix)
        with open("tfidf_"+finame, "wb") as f:
            pickle.dump(paths, f)
            pickle.dump(vectorizer, f)
            pickle.dump(tfidf_matrix, f)

    print(f'{time.time()-wow} time to generate')

def load_tensors(finame='yayayay', tensors=False):
    objects = []
    if tensors:
        with (open('tensors_'+finame, "rb") as openfile):
            while True:
                try:
                    content = pickle.load(openfile)
                    objects.append(content)
                except EOFError:
                    break

    with (open('tfidf_'+finame, "rb") as f):
        paths = pickle.load(f)
        vectorizer = pickle.load(f)
        tfidf_matrix = pickle.load(f)
        
    return objects, paths, vectorizer, tfidf_matrix