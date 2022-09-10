import cv2
import matplotlib.pyplot as plt
import numpy as np


def negativo(imagem):
    for x in range(0,imagem.shape[0]):
        for y in range(0, imagem.shape[1]):
            imagem[x,y] = 255 - imagem[x,y]
    return imagem


def threshold(img,valfoto,valthresh):
    for x in range(0,img.shape[0]):
        for y in range(0, img.shape[1]):
            if img[x,y]!= valfoto:
                img[x,y] = valthresh
    return img


def thresholdIgualado(img,valfoto,valthresh):
    for x in range(0,img.shape[0]):
        for y in range(0, img.shape[1]):
            if img[x,y] == valfoto:
                img[x,y] = valthresh
    return img


def RemovePontosPretos(imagem):
    imagemOriginal = cv2.imread(imagem)
    img = cv2.imread(imagem)
    image = negativo(img)
    elemestruturante = np.ones((3,3),np.uint8)
    erosao = cv2.erode(image,elemestruturante,iterations=9)
    image = negativo(erosao)
    cv2.imwrite('ImagemSemPontosPretos.png',image)
    cv2.imshow("ImagemOriginal / ImagemSemPontosPretos", np.hstack((imagemOriginal, image)))
    cv2.waitKey(0)

    
def PreencheBuracos():
    ImagemOriginal = cv2.imread("ImagemSemPontosPretos.png")
    img = cv2.imread("ImagemSemPontosPretos.png")
    imagem = negativo(img)
    elemestruturante = np.ones((5,5),np.uint8)
    dilatacao = cv2.dilate(imagem,elemestruturante,iterations=16)
    imagem = negativo(dilatacao)
    cv2.imshow("ImagemOriginal / ImagemPreenchida", np.hstack((ImagemOriginal, imagem)))
    cv2.imwrite('ImagemPreenchida.png',imagem)
    cv2.waitKey(0)
    

def FechoConvexo(intensidade,arraycor,nomefoto):
    image = cv2.imread('ImagemPreenchida.png')
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = thresholdIgualado(img,0,76)
    imagem = threshold(img,intensidade,255)
    tresh = thresholdIgualado(imagem,intensidade,0)
    contours, hierarchy = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        cv2.drawContours(image, [hull], -1, arraycor, 2)
    cv2.imwrite(nomefoto,image)
    cv2.imshow('Fecho convexo', image)
    cv2.waitKey(0)
    
    
def EsqueletoDaImagem(nomeimg, intensidade):
    
    img = cv2.imread('ImagemPreenchida.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = thresholdIgualado(img,0,76)
    imagem = threshold(img,intensidade,255)
    img = thresholdIgualado(imagem,intensidade,0)
    img = negativo(img)
    esqueleto = np.zeros(img.shape, np.uint8)
    elemestruturante = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    while True:
        open = cv2.morphologyEx(img, cv2.MORPH_OPEN, elemestruturante)
        subtracao = cv2.subtract(img, open)
        eroded = cv2.erode(img, elemestruturante)
        esqueleto = cv2.bitwise_or(esqueleto, subtracao)
        img = eroded.copy()
        if cv2.countNonZero(img) == 0:
            break
        
    cv2.imshow('imagem', esqueleto)
    cv2.imwrite(nomeimg, esqueleto)
    cv2.waitKey(0)
    
def FazHitOrMiss():
    imgOriginal = cv2.imread("ImagemPreenchida.png")
    imgOriginal = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
    imgOriginal = thresholdIgualado(imgOriginal,0,76)
    img = threshold(imgOriginal,76,255)
    img = thresholdIgualado(img,76,0)
    img = negativo(img)
    elemestruturante = np.array(([1,1,1],[1,1,1],[1,1,1]), dtype=int)
    SaidaHitOrMiss = cv2.morphologyEx(img, cv2.MORPH_HITMISS, elemestruturante)
    cv2.imwrite('SaidaHitOrMiss.png', SaidaHitOrMiss)
    cv2.imshow('HitOrMiss', SaidaHitOrMiss)
    cv2.waitKey(0)
        
def main(): 
    azul = 29
    verde = 150
    vermelho = 76
    amarelo = 226
    intensidade = [azul, vermelho, verde, amarelo]
    
    #1. REMOVER PONTOS PRETOS
    #RemovePontosPretos()
    
    #2. PRRENCHER OS BURACOS
    #PreencheBuracos()
    
    #3. FECHOS CONVEXOS
    #Para o azul
    #FechoConvexo(intensidade[0], [255,0,0], 'FechoConvexoAzul.png')
    #Para o verde
    #FechoConvexo(intensidade[2], [0,255,0], 'FechoConvexoVerde.png')
    #Para o amarelo
    #FechoConvexo(intensidade[3],[255,0,255], 'FechoConvexoAmarelo.png')
    
    #4. ESQUELETOS DAS IMAGENS
    #EsqueletoDaImagem('EsqueletoVerde.png',intensidade[2])
    #EsqueletoDaImagem('EsqueletoAzul.png',intensidade[0])
    #EsqueletoDaImagem('EsqueletoAmarelo.png',intensidade[3])
    
    #5. HIT OR MISS OBJETOS VERMELHOS
    #FazHitOrMiss()
    
main()





