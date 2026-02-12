from fastapi import FastAPI, Query, Body, HTTPException, Path
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List, Union, Literal
from math import ceil

app = FastAPI(title="Mini Blog")

BLOG_POST=[
    {"id":1,"title": "Hola desde FastAPI","content":"Mi primer post con fastapi"},
    {"id":2, "title": "Hola desde ajonjoli", "content":"Mi segundo post con fastapi"},
    {"id":3, "title": "Hola desde pello", "content":"Mi tercero post con fastapi"},
    {"id":4,"title": "Hola desde FastAPI","content":"Mi primer post con fastapi"},
    {"id":5, "title": "Hola desde ajonjoli", "content":"Mi segundo post con fastapi","tags":[{"name":"Python"},{"name":"pello"}]},
    {"id":6, "title": "Hola desde pello", "content":"Mi tercero post con fastapi"},
    {"id":7,"title": "Hola desde FastAPI","content":"Mi primer post con fastapi"},
    {"id":8, "title": "Hola desde ajonjoli", "content":"Mi segundo post con fastapi"},
    {"id":9, "title": "Hola desde pello", "content":"Mi tercero post con fastapi", "tags":[{"name":"Python"},{"name":"pello"}]},
    {"id":10,"title": "Hola desde FastAPI","content":"Mi primer post con fastapi"},
    {"id":11, "title": "Hola desde ajonjoli", "content":"Mi segundo post con fastapi","tags":[{"name":"Python"},{"name":"pello"}]},
    {"id":12, "title": "Hola desde pello", "content":"Mi tercero post con fastapi"}
]
# Definimos las palabras prohibidas (en minúsculas)
BANNED_WORDS = {"xxx", "porn", "dick", "sex", "spam"}
#clases de modelos creados con pydantic

class Tag(BaseModel):
    name: str= Field(..., min_length=2, max_length=30, description="Nombre de la etiqueta")

class Autor(BaseModel):
    name: str= Field(..., min_length=2, description="Autor del post")
    email: EmailStr
    
class PostBase(BaseModel):
    title: str
    content: str
    #default_factory hace una lista nueva por cada objeto que se cree
    tags: Optional[List[Tag]] = Field(default_factory=list)#[]
    autor: Optional[Autor]= None
    
class PostCreate(BaseModel):
    title: str = Field(
        #Field da la posibilidad de añadir validaciones más avanzadas
        #Elipsis, es obligatorio, espera contenido
        ...,
        min_length=3,
        max_length=100,
        description="Titulo del post (mínimo 3 caracteres y maximo 100)",
        examples=["Mi primer post con FastAPI"]
    )
    content: Optional[str] = Field(
        default="Contenido predeterminado",
        min_length=10,
        description="Contenido del post, minimo 10 caracteres",
        examples=["Esto es un ejemplo"]
    )
    tags: List[Tag] = Field(default_factory=list)#[]
    autor: Autor = None

    @field_validator("title")
    @classmethod
    def not_allowed_title(cls, value: str) -> str:
        for word in BANNED_WORDS:
            if word in value.lower():
                raise ValueError(f"Es titulo no puede contener la palabra {word}")
        return value
        
class PostUpdate(BaseModel):
    title: Optional [str]
    content: Optional[str] = None #"Valor por defecto"
    
class PostPublic(PostBase):
    id: int

class PostSummary(BaseModel):
    id: int
    title: str
    
class PaginatedPost(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id","title"]
    direction: Literal["asc","desc"]
    search: Optional[str] = None
    items: List[PostPublic]
    
    
@app.get("/")
def home():
    return {'message':'Bienvenidos a Mini Blog por Pello'}


@app.get("/posts", response_model=PaginatedPost)
def list_posts(
    text: Optional[str]= Query(
        default=None,
        deprecated=True,
        description="Obsoleto, usa query o search en su lugar"
    ),
    query: Optional[str]= Query(
        default=None,
        description="Texto para buscar por titulo",
        alias="search",#muestra este nombre al cliente
        min_length=3,
        max_length=50,
        pattern= r"^[\w\sáéíóúÁÉÍÓÚüÜ-]+$"
    ),
    per_page: int = Query(
        10, ge=1,le=50,
        description="Numero de resultados (1-50)"
    ),
    page: int= Query(
        1, ge=1,
        description="Numero de paginas (>=1)"
    ),
    order_by: Literal["id","title"] = Query(
        "id",description="Campo de orden"
    ),
    direction:Literal["asc","desc"]= Query(
        "asc", description="Direccion de orden"
)
):
    results = BLOG_POST
    
    query = query or text
#query parameters los usamos para filtrar
#path parametros para buscar exactamente
    if query:
        results = [post for post in BLOG_POST if query.lower()
                   in post["title"].lower()]
    total=len(results)
    #ceil redonde hacia abajo o arriba un decimal
    total_pages= ceil(total/per_page) if total > 0 else 0
    
    if total_pages == 0:
        current_page = 1
    else:
        current_page = min(page, total_pages)
        #sorted() ordena
    results= sorted(
        results, key=lambda post: post[order_by], reverse=(direction == "desc")) 
    
    if total_pages == 0:
        items = []
    else:
        start = (current_page - 1)* per_page
        items = results[start: start+per_page]
        
    #Lambda es una funcion anonima que se ejecuta en ese momoento
        # for post in BLOG_POST:
        #     if query.lower() in post["title"].lower():
        #         results.append(post)
        # return {"data": results, "query": query}
    has_prev = current_page > 1
    has_next = current_page < total_pages if total_pages > 0 else False
    
    return PaginatedPost(total=total, 
                         per_page=per_page, 
                         page=current_page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next,
                         order_by=order_by,
                         direction=direction,
                         search=query,
                         items=items)
        #response_model nos permite mandar diccionario 
    
 
@app.get("/post/by-tags", response_model=List[PostPublic])
def filter_by_tags(
    tags: List[str]= Query(
        ...,
        min_length=2,
        description="Una o mas etiquetas. Ejemplo: ?tags=python&tags=fastapi"
    )
):
    tags_lower = [tag.lower() for tag in tags]
    
    return [
        post for post in BLOG_POST if any(tag["name"].lower() in tags_lower for tag in post.get("tags" , []) )
    ]
#Union usamos para agregar dos modelos y que fastapi los evalue en orden y elige el que hace macht, es como un switch 
@app.get("/posts/{post_id}", response_model=Union[PostPublic,PostSummary], response_description="Post econtrado")
def get_post(post_id: int = Path(
        ...,#esperamos contenido
        ge=1,
        title= "ID del post",
        description="Identificador entero del post. Debe ser mayor a 1",
        example=1
    ), include_content: bool = Query(default=True, description="Mostrar contenido")):
    for post in BLOG_POST:
        if post["id"] == post_id:
            if not include_content:
                return {"id": post["id"], "title": post["title"]}
            return post
    raise HTTPException(status_code=404, detail="Post no encontrado")


@app.post("/posts", response_model=PostPublic, response_description="Post creado (OK)")
#elipsis = ... significa que es obligatorio, None que es opcional
#post: dict= Body(...)
def create_post(post: PostCreate):

    # if "title" not in post or "content" not in post:
    #     return {"error": "Title y content son requeridos"}
    # #.strip quita todos los espacios en blanco
    # if not str(post["title"]).strip():  
    #     return {"error": "Title no puede estar vacío"}
    new_id= (BLOG_POST[-1]["id"]+1) if BLOG_POST else 1
    new_post = {"id": new_id,
                "title": post.title,
                "content": post.content,
                "tags": [tag.model_dump() for tag in post.tags],
                "autor": post.autor.model_dump() if post.autor else None}#Esta forma de crear listas se conoce como list comprehension
    BLOG_POST.append(new_post)
    return new_post


#response_description define el mensaje que devuelve return
#response_model_exclude_none define si queremos ver vacios o no
@app.put("/posts/{post_id}", response_model=PostPublic, response_description="Post actualizado (OK)", response_model_exclude_none=True)
#data: dict = Body(...)
def update_post(post_id: int, data: PostUpdate):
    for post in BLOG_POST:
        if post["id"] == post_id:
            #model_dump() convierte a diccionario, exclude_unset excluye valores que no ponemos, asi evitamos sobrescrituras none
            playload = data.model_dump(exclude_unset=True) #{"title"}: "Ivan", {"content"}: None
            if "title" in playload: post["title"]= playload["title"]
            if "content" in playload: post["content"]= playload["content"]
            return post
        
    raise HTTPException(status_code=404, detail="Post no encontrado")


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    for index, post in enumerate(BLOG_POST):
        if post["id"]== post_id:
#.pop Remove and return item at index (default last).
            BLOG_POST.pop(index)
            return
    raise HTTPException(status_code=404, detail="Post no encontrado")


#DOCUMENTACIONES AUTOMATICAS
#/docs
#/redoc