# Create containers
## Build
```bash
docker-compose down
docker-compose up -d --build
```

## Scale
If you want scale inferency mortor to 5 new containers use it
```bash
docker-compose up -d --scale inferency_motor=5
```

## Stop
```bash
docker-compose down
```

# API REST USE

## User

### POST

#### user/taxonomic_route
Se envia una imagen y se espera una respuesta del servidor. El servidor analizará la imagen buscando todos los posibles organismos que se encuentren en la misma y será analizados por separado.

**Envio:** 
```json
{
    "image": "image in base64" 
}
```
**recepción:**
```json
{
    "identifiers": [
        {
            "class": "class_name",
            "order": "order_name",
            "family": "family_name",
            "genus": "genus_name",
            "specie": "specie_name",
            "top5_specie": ["specie1", "specie2", "specie3", "specie4", "specie5"],
            "message": "response_message"
        },
        {
            "class": "class_name",
            "order": "order_name",
            "family": "family_name",
            "genus": "genus_name",
            "specie": "specie_name",
            "top5_specie": ["specie1", "specie2", "specie3", "specie4", "specie5"],
            "message": "response_message"
        }
    ]
    
}

```


#### user/taxonomic_routes
Se envia una imagen y se espera una respuesta del servidor. 

**Envio:**
```json
{
    "images":
    [
        {
            "image": "image(base64)"
        },
        {
            "image": "image(base64)"
        },
    ] 
}
```
**Recepción:**
```json
{
    "class": "class_name",
    "order": "order_name",
    "family": "family_name",
    "genus": "genus_name",
    "specie": "specie_name",
    "top5_specie": ["specie1", "specie2", "specie3", "specie4","specie5"],
    "message": "response_message"
}
```

## Admin

### POST

