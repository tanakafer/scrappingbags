import os
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from argparse import ArgumentParser
from slugify import slugify
import re
from PIL import Image
import datetime


parser = ArgumentParser(description='Convertir un directory de imágenes un dataset en csv')

parser.add_argument(
    '-d', '--directory', required=True,
    help='Localización del directorio de imágenes' , type=str)

parser.add_argument(
    '-t', '--test_size', required=False,  type=float, default =0.2,
    help='Porcentaje que separamos para el test' )

parser.add_argument(
    '-b', '--basewidth', required=False, type=float, default=600,
    help='Ancho para redimensionar y mantener ratio' )


def main(argv):
    root_directory = argv.directory
    test_size = argv.test_size
    basewidth = argv.basewidth


    directory = os.path.join(root_directory,'images')

    files_withoutnumber = []
    size_files = []
    labels = []
    dataset = []
    errors = []


    # Recorremos todos los directorios
    for root, dirs, files in os.walk(directory, topdown=True):
        for path in dirs:
            dir = os.path.basename(path)
            dir_old = dir
            # Normalizamos el nombre del directorio
            dir = slugify(dir)
            os.rename(os.path.join(root,dir_old),os.path.join(root, dir) )
            labels.append(dir)
        for file in tqdm(files, desc = 'Files {}'.format(root)):

            remove = False
            class_dir = os.path.basename(root)
            pid = labels.index(class_dir) +1
            # Normalizamos el fichero
            # eliminando comas
            file_old, fileExtension = os.path.splitext(file)
            file =slugify(file_old)

            # Comprobamos que el fichero con el mismo nombre
            # y con el mismo tamaño se elimine
            # para no tener imágenes repetetidas
            file_old =file_old +  fileExtension
            file_new = file +  '.jpg'
            size_file =os.path.getsize(os.path.join(root,file_old))
            regex = r'[0-9]*-(\S+)$'
            file_withoutnumber = re.findall(regex, file)
            if  len(file_withoutnumber) >0:
                file_withoutnumber= file_withoutnumber[0]
            else:
                file_withoutnumber =class_dir +  str(datetime.date)

            if  file_withoutnumber in files_withoutnumber:
                index = files_withoutnumber.index(file_withoutnumber)
                file_check = files_withoutnumber[index]
                size_check = size_files[index]

                # print ("Fichero: {} Anterior: {}".format(file_withoutnumber, file_check))
                # print ("Fichero: {} Anterior: {}".format(size_file, size_check))
                if size_check == size_file:
                    fid = os.path.join(root,file_old)
                    remove = True

            if not remove:
                files_withoutnumber.append(file_withoutnumber)
                size_files.append(size_file)
                #Convertimos las imágenes a jpg
                try:

                    im = Image.open(os.path.join(root,file_old))
                    # Redimensionamos para ahorrar espacio
                    # EL redimensionado definito lo hacemos en el modelo
                    im = resize_img(basewidth, im)
                    rgb_im= im.convert('RGB')
                    rgb_im.save(os.path.join(root,file_old), 'JPEG' )
                    os.rename(os.path.join(root,file_old),os.path.join(root,file_new ))
                    #os.remove(os.path.join(root,file_old +  fileExtension))
                    fid = os.path.join(class_dir, file_new)
                    # No añadimos las imágenes que no son git, jpeg o png
                    # o dan un error
                    dataset.append([pid, fid])
                except:
                    fid = os.path.join(root,file_new)
                    remove = True

            if remove:
                # os.remove(fid)
                print('La imagen {} no se añadió y se eliminó'.format(fid))
                errors.append([pid,fid])


    print("Labels numbers: {}".format(len(labels)))
    labels = pd.DataFrame(labels)
    labels.index = labels.index + 1
    labels.to_csv(os.path.join(root_directory, 'bags_labels.csv'), sep=',', header=None,  encoding='utf-8')
    ds = np.array(dataset)
    if test_size and ds.shape[0]>100:
        # Cogemos los identificadores de i
        X = [ i for i in np.arange(ds.shape[0])]
        Y = ds[:,0]
        x_train,  x_test, y_train,  y_test = train_test_split(X, Y, test_size=test_size)
        fid_train=ds[x_train,1]
        fid_test=ds[x_test,1]
        pid_train=y_train
        pid_test=y_test

        train = pd.DataFrame( {'pid': pid_train, 'fid': fid_train})
        test = pd.DataFrame( {'pid': pid_test, 'fid': fid_test})        #train = np.concatenate(y_train, x_train)
        train.to_csv(os.path.join(root_directory, 'bags_train.csv'), sep=',', header=None,  index = False, encoding='utf-8')
        test.to_csv(os.path.join(root_directory,'bags_test.csv'), sep=',', header=None,  index = False, encoding='utf-8')


    dataset = pd.DataFrame(dataset)
    dataset.to_csv(os.path.join(root_directory,'bags_dataset.csv'), sep=',', header=None,  index = False, encoding='utf-8')
    errors = pd.DataFrame(errors)
    errors.to_csv(os.path.join(root_directory,'errors.csv'), sep=',', header=None,  index = False, encoding='utf-8')



def resize_img(basewidth, img):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    return img


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
