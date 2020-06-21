#ScrappingBags

Este repositorio realiza una descarga de imágenes de internet desde el buscador Bing de bolsos

Este código está basado en la adaptación realizada por  Evan Sellers <sellersew@gmail.com> en Febrero de 2020 para buscar en Bing y en la adaptación de glenn.jocher@gmail.com Feb 2020 para su utilización den python 3.
El código original se puede encontrar en https://github.com/hardikvasa/google-images-download


# Requerimientos

- Python 3+ [Comprobado en 3.6.9/3.7.5]

# Utilización

Editar el campo 'output_directory' en los ficheros Famous_bags_40.json y Famous_bagas.json  para determinar el directorio donde se descargarán las imágenes.

Una vez modificado dichos ficheros ejecutar

'''
  python3 famous_bags.py
'''


'''
  python3 famous_bags_40.py
'''


Finalizado el proceso de descarga se tendrá que realizar una limpieza del conjunto de imágenes con el comando directory2csv.py. Seleccionando el directorio donde se almacenan las imágenes.

Este comando realiza una limpieza de las imágenes con dos criterios:

- Sean ficheros de formatos jpeg, gif y png.
- El nombre y  el tamaño coincida, para evitar los duplicados.


Además el comando hace una limpieza en el nombre com slugify, por defecto separa el 20% de la imágenes para su evaluación aunque es configurable y redimensiona el tamaño de las imágenes a un ancho de 600 pixeles, esto también es configurable.
