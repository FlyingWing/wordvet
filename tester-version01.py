#!/Users/fa/anaconda/bin/python

    
from gensim import corpora, models, similarities
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import matplotlib.pyplot as plt
import numpy as np
import bisect 
import math

 
import multiprocessing
import openpyxl 
import os
import sys
import subprocess
import docopt
import datetime


from scipy import spatial
from sklearn.preprocessing import normalize


'''''
def similarities1(wordpairFile, goldScoreFile, modelFiles,  outputFile):
    outf = open(outputFile, 'w')
    models = list()
    for modelFile in modelFiles:
        print(modelFile)
        models.append ( Word2Vec.load_word2vec_format(modelFile, binary=False) ) # C text format
    print("FA: similarities!")
   
    wordpairs = [line.rstrip('\n') for line in open(wordpairFile)]
    goldScores = [line.rstrip('\n') for line in open(goldScoreFile)]
    for index, pair in enumerate(wordpairs):
        words = pair.split('\t')
        print(words)
        outf.write( words[0] + "\t" + words[1] + "\t" + goldScores[index] + "\t")
        for model in models:
            if(words[0] in model.vocab and words[1] in model.vocab):
                score = ( model.similarity(words[0], words[1]) * 2.0 ) + 2
            else:
                score = 0
            outf.write( str(score) + "\t" )
        outf.write( str(score) + "\n" )
    outf.close()
    return similarities
    
def test(wordpairFile, goldScoreFile, modelRepository, outputFile):
    modelFiles = list()
    for dirName, dirNames, fileNames in os.walk(modelRepository):
        # print path to all filenames.
        for fileName in fileNames:
            if "DS_Store" not in fileName:
                print(os.path.join(dirName, fileName))
                modelFiles.append(os.path.join(dirName, fileName))
    
    similarities1(wordpairFile, goldScoreFile, modelFiles, outputFile)
    return 0
'''   
    

def similarities(wordpairFile, modelWord, modelContext,  outputFile, formula = "ww"):
    outf = open(outputFile, 'w')
    mw = modelWord
    mc = modelContext
    print("FA: similarity calculation with formula: " + formula)
    wordpairs = [line.rstrip('\n') for line in open(wordpairFile)]
    for index, pair in enumerate(wordpairs):
        words = pair.split('\t')
        
        score = 0.0
        if(words[0] in mw.vocab and words[1] in mw.vocab):
            w0 = mw[words[0]]
            w1 = mw[words[1]]
            c0 = mc[words[0]]
            c1 = mc[words[1]]
            b0 = np.add(mw[words[0]] , mc[words[0]])
            b1 = np.add(mw[words[1]] , mc[words[1]])
            wwScore = 1 - spatial.distance.cosine(normalize(w0[:,np.newaxis], axis=0).ravel(), normalize(w1[:,np.newaxis], axis=0).ravel() )
            ccScore = 1 - spatial.distance.cosine(normalize(c0[:,np.newaxis], axis=0).ravel(), normalize(c1[:,np.newaxis], axis=0).ravel() )
            wcScore = 1 - spatial.distance.cosine( normalize(w0[:,np.newaxis], axis=0).ravel(), normalize(c1[:,np.newaxis], axis=0).ravel() )
            cwScore = 1 - spatial.distance.cosine( normalize(w1[:,np.newaxis], axis=0).ravel(), normalize(c0[:,np.newaxis], axis=0).ravel() )
            bbScore = 1 - spatial.distance.cosine(normalize(b0[:,np.newaxis], axis=0).ravel() , normalize(b1[:,np.newaxis], axis=0).ravel() )
            if formula == "ww" : score = wwScore 
            elif formula == "cc" : score = ccScore
            elif formula == "wc" : score = wcScore
            elif formula == "cw" : score = cwScore
            elif formula == "bb" : score = bbScore
            elif formula == "v2" :
                if ( bbScore > wwScore ) : #relatedness is bigger than similarity
                    score = 0.9 * wwScore
                elif ( bbScore < wwScore ) : 
                    score = 1.1 * wwScore
            else: print("Error!")
        outf.write( str(score) + "\n")
    outf.close()
    return similarities
    
    
       
    
def train(textRepository, modelRepository):
    # Trains word2vec model on text files from textRepository
    # Creates vectorsW.txt and vectorsC.txt in modelRepository    
    return 0



def test(modelRepository, inputPath , outputPath):
    # Uses the models in the modelRepository for similarity inference (different formulas)
    # Creates similarity score files in the outputPath
    
    modelW = modelRepository + "vectorsW.txt"
    modelC = modelRepository + "vectorsC.txt"
    mw =  Word2Vec.load_word2vec_format(modelW, binary=False) 
    mc =  Word2Vec.load_word2vec_format(modelC, binary=False)
    
    
    for formula in ["ww","cc","wc","cw","bb", "v2"]:
        similarities(inputPath, mw, mc, outputPath + formula + ".txt" , formula)
           
           
           
    
import getopt

def main(argv):
    modelRepository = "/Users/fa/workspace/repos/_codes/MODELS/text8exp/-cbow0-size100-window5-negative5-hs1-sample0-threads10-binary0-iter1/"
    inputPath = "/Users/fa/workspace/repos/_codes/sharedTask/subtask1-monolingual/data/en.trial.data.txt"
    outputPath = "/Users/fa/workspace/repos/_codes/sharedTask/subtask1-monolingual/output/en.out-"
    try:
        opts, args = getopt.getopt(argv,"hm:i:o:",["mrepos=","ifile=","ofile="])
        print(opts)
        print(args)
    except getopt.GetoptError:
        print 'test.py -m <modelrepos> -i <inputfile> -o <outputfile(s)>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -m <modelrepos> -i <inputfile> -o <outputfile(s)>'
            sys.exit()
        elif opt in ("-m", "--mrepos"):
            modelRepository = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    test(modelRepository, inputPath , outputPath)
    

if __name__ == "__main__":
   main(sys.argv[1:])
   