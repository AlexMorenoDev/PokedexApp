# POKÉDEX APP
Aplicación web hecha como hobby que consiste en una Pokédex que permite visualizar de diferentes maneras la información acerca de todos los Pokémon que existen hasta el día de hoy. Cabe destacar que la aplicación no está completa y a lo largo del tiempo ser irá actualizando con nuevas funcionalidades o mejoras.

## Descripción 
La aplicación está compuesta por una vista en la que se muestra el listado completo de los Pokémon (formato de cartas). En cada carta, se visualizan la imagen del Pokémon y algunos datos básicos: id, nombre y tipos. 

Además del listado, forma parte de la aplicación la vista de detalle, a la que se puede acceder a través de cada carta de Pokémon haciendo clic en el botón "+" o encima de la imagen del Pokémon en cuestión. Dentro de la página de detalle, se muestran todos los datos referentes al Pokémon: id, nombre, tipos, habilidades, grito, cadena evolutiva, etc.

## Tecnologías utilizadas
- Frontend:
    - HTML
    - JavaScript
    - CSS
    - [Bootstrap 5](https://getbootstrap.com/) - [Autocomplete plugin](https://github.com/Honatas/bootstrap-4-autocomplete)
    - [Font Awesome 4](https://fontawesome.com/v4/)
- Backend:
    - [Python](https://www.python.org/)
    - [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- Datos (guardados localmente y obtenidos a través de la [Pokéapi](https://pokeapi.co/)):
    - Archivos JSON.
    - Imágenes en formato PNG y GIF.
    - Sonidos en formato OGG y MP3.

**Nota sobre los datos**: Los datos y archivos multimedia se generan ejecutando el script "src/scripts/init_model.py", y se guardan en la carpeta "static/pokemon/". El script "src/scripts/download_media_and_data.py" se utiliza únicamente en el proceso de despliegue.

## Despliegue
El despliegue se ha hecho en una instancia gratuita de [Render](https://render.com/). Cabe destacar que a la hora de desplegar la aplicación, como el script "src/scripts/init_model.py" tarda en finalizar su ejecución al completo, se ha optado por ejecutarlo primero en local de la siguiente manera:
1. Tras la finalización del script se comprime la carpeta "static/pokemon/" generada.
2. Se sube a google drive el archivo comprimido en formato ".zip" y se modifica el modo de compartición del archivo para que pueda accederse a él a través de un enlace.
3. En el proceso de despliegue en Render es necesario definir una variable de entorno llamada "gdrive_file_id" que contenga el id del enlace compartido que apunte al archivo de google drive. El id sería lo que está entre los signos "<" y ">":
https[]()://drive.google.com/file/d/**<gdrive_file_id>**/view?usp=sharing
4. Se ejecuta en el despliegue el script "src/scripts/download_media_and_data.py" para descargar y extraer el contenido del archivo comprimido dentro de la instancia de Render. 

La aplicación está disponible en el siguiente [enlace](https://alxpokedexapp.onrender.com/).

## Copyright
- This is just a fan-made project for educative and informational purposes, no copyright infringement intended. / Esto es solo un proyecto hecho por un fan con fines educativos e informativos, no se pretende infringir los derechos de autor.

- All media contents and data within "static/pokemon/" folder (generated by "init_model.py" or "download_media_and_data.py" scripts) are copyrighted by The Pokémon Company, Nintendo, Creatures Inc., Game Freak and its affiliates. / Todos los archivos multimedia y datos dentro de la carpeta "static/pokemon/" (generados por los scripts "init_model.py" o "download_media_and_data.py") son propiedad de The Pokémon Company, Nintendo, Creatures Inc., Game Freak y sus afiliados: 
    - [The Pokémon Company](https://www.pokemon.com/)
    - [Nintendo](https://www.nintendo.com/)
    - [Creatures Inc.](https://www.creatures.co.jp/)
    - [Game Freak](https://www.gamefreak.co.jp/)

- All media contents and data within "static/pokemon/" folder (generated by "init_model.py" or "download_media_and_data.py" scripts) were downloaded through the URLs defined in Pokéapi service for each pokemon, evolution chain... / Todos los archivos multimedia y datos de los pokemon guardados dentro de "static/pokemon/" (generados por los scripts "init_model.py" o "download_media_and_data.py") se han descargado a través de los enlaces que se pueden consultar en la Pokéapi para cada pokemon, cadena evolutiva...:
    - [Pokéapi](https://pokeapi.co/)

- "static/pokeball.png" --> Image by '[Harisankar Sahoo](https://pixabay.com/users/hsaart-8633812/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4657023)' from [Pixabay](https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4657023) / Imagen hecha por '[Harisankar Sahoo](https://pixabay.com/users/hsaart-8633812/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4657023)' y descargada de [Pixabay](https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4657023): 
    - [Image](https://pixabay.com/vectors/pokemon-icon-design-symbol-sign-4657023/)

- Any other files, data or media within this repository that are copyrighted and not mentioned above, are the property or trademarks of their respective owners. / Cualquier otro archivo, datos o multimedia dentro de este repositorio que tenga copyright y que no haya sido mencionado anteriormente, son propiedad o marcas registradas por sus respectivos dueños.

## Capturas

![(Imagen no encontrada - Página listado)](repo_images/listado_pokemon.png)

---

![(Imagen no encontrada - Página detalle 1)](repo_images/detalle_pokemon_1.png)

---

![(Imagen no encontrada - Página detalle 2)](repo_images/detalle_pokemon_2.png)

---

![(Imagen no encontrada - Footer)](repo_images/footer.png)
