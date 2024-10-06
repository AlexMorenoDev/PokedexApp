
pkm_id_start = 1
#pkm_id_end = 151
pkm_id_end = 1025
remove_pokemon_info = False # If pokemon info JSON files must be generated again set it to true
remove_pokemon_evolution_chain = False # If pokemon evolution chain JSON files must be generated again set it to true

pokemon_info_path = "../../static/pokemon/info/"
pokemon_evolution_chains_path = "../../static/pokemon/evolution_chains/"
pokemon_dirs = [
    pokemon_info_path,
    pokemon_evolution_chains_path,
    "../../static/pokemon/cries/ogg/", 
    "../../static/pokemon/images/normal/", 
    "../../static/pokemon/images/shiny/",
    "../../static/pokemon/sprites/no_animated/normal/front/male/",
    "../../static/pokemon/sprites/no_animated/normal/back/male/",
    "../../static/pokemon/sprites/no_animated/normal/front/female/",
    "../../static/pokemon/sprites/no_animated/normal/back/female/",
    "../../static/pokemon/sprites/no_animated/shiny/front/male/",
    "../../static/pokemon/sprites/no_animated/shiny/back/male/",
    "../../static/pokemon/sprites/no_animated/shiny/front/female/",
    "../../static/pokemon/sprites/no_animated/shiny/back/female/",
    "../../static/pokemon/sprites/animated/normal/front/male/",
    "../../static/pokemon/sprites/animated/normal/back/male/",
    "../../static/pokemon/sprites/animated/normal/front/female/",
    "../../static/pokemon/sprites/animated/normal/back/female/",
    "../../static/pokemon/sprites/animated/shiny/front/male/",
    "../../static/pokemon/sprites/animated/shiny/back/male/",
    "../../static/pokemon/sprites/animated/shiny/front/female/",
    "../../static/pokemon/sprites/animated/shiny/back/female/"
]

objects_dir = "../../static/objects/sprites/"

trigger_translations = {
    "level-up": "Subir de nivel", 
    "trade": "Intercambio",
    "use-item": "Usar objeto", 
    "shed": "Un espacio en el equipo y tener una pokeball", 
    "tower-of-darkness": "Entrenar en la torre de la oscuridad",
    "tower-of-water": "Entrenar en la torre de las aguas", 
    "three-critical-hits": "Asestar tres golpes críticos en un combate"
}

evolution_keys_translations = {
    "gender": "Sexo",
    "held_item": "Objeto equipado",
    "item": "Objeto",
    "known_move": "Movimiento aprendido",
    "known_move_type": "Tipo de movimiento aprendido",
    "location": "Localización",
    "min_affection": "Nivel de afecto",
    "min_beauty": "Nivel de belleza",
    "min_happiness": "Nivel de felicidad",
    "min_level": "Nivel",
    "needs_overworld_rain": "Lluvia",
    "party_species": "Pokemon en el equipo",
    "party_type": "Tipo de pokemon en el equipo",
    "relative_physical_stats": "Estadísticas",
    "time_of_day": "Hora del día",
    "trade_species": "Pokemon intercambiado",
    "trigger": "Desencadenante",
    "turn_upside_down": "Poner boca abajo la consola"
}
