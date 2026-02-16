
import os
from datetime import datetime
from fastapi import FastAPI, Query, Body, HTTPException, Path, status, Depends
from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from typing import Optional, List, Union, Literal
from math import ceil
from sqlalchemy import create_engine, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL= os.getenv("DATABASE_URL","sqlite:///./blog.db")
print("Conectado a:", DATABASE_URL)
app = FastAPI(title="Mini Blog")

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"]={"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, future=True, **engine_kwargs)#Opcional con postgre sql

SessionLocal = sessionmaker(
    bind = engine, autoflush=False, autocommit= False, class_=Session)#Autoflush, no envia cambio hasta hacer commit

class Base(DeclarativeBase):
    pass


class PostORM(Base):
    __tablename__= "post"
     #mapped representacion de tipo y mapped_colum representador
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine) #dev,crear tablas para desarrollo (si no existen), en produccion usaremos migraciones

def get_db():
    db = SessionLocal()
    try:
        yield db #yield sirve para asegurar que el programa pause hasta que se ejecute y ya despues entra al finally
    finally:
        db.close()

BLOG_POST = [
    {
        "id": 1,
        "title": "Introducción a FastAPI: El framework más rápido de Python",
        "content": "FastAPI es un framework moderno y rápido para construir APIs con Python 3.7+ basado en estándares como OpenAPI y JSON Schema. En este post exploraremos sus características principales y por qué está ganando tanta popularidad en la comunidad de desarrolladores.",
        "tags": [{"name": "FastAPI"}, {"name": "Python"}, {"name": "Backend"}],
        "autor": {"name": "Ana García", "email": "ana.garcia@devblog.com"},
        "created_at": "2024-01-15"
    },
    {
        "id": 2,
        "title": "Validación de datos con Pydantic: Guía completa",
        "content": "Pydantic es la librería de validación de datos más popular de Python. Aprende a usar modelos, validadores personalizados, y cómo integrarlo perfectamente con FastAPI para crear APIs robustas y type-safe.",
        "tags": [{"name": "Pydantic"}, {"name": "Python"}, {"name": "Validación"}],
        "autor": {"name": "Carlos Ruiz", "email": "carlos.ruiz@devblog.com"},
        "created_at": "2024-01-22"
    },
    {
        "id": 3,
        "title": "Async vs Sync en Python: Cuándo usar cada uno",
        "content": "El modelo asíncrono de Python puede ser confuso al principio. En este artículo desglosamos las diferencias entre programación síncrona y asíncrona, cuándo aplicar async/await y cómo FastAPI aprovecha esto para alto rendimiento.",
        "tags": [{"name": "Python"}, {"name": "Async"}, {"name": "Performance"}],
        "autor": {"name": "María López", "email": "maria.lopez@devblog.com"},
        "created_at": "2024-02-05"
    },
    {
        "id": 4,
        "title": "Deploy de FastAPI con Docker y Docker Compose",
        "content": "Llevar tu aplicación FastAPI a producción no tiene por qué ser complicado. Te mostramos paso a paso cómo containerizar tu API, configurar Uvicorn/Gunicorn y orquestar servicios con Docker Compose.",
        "tags": [{"name": "Docker"}, {"name": "DevOps"}, {"name": "FastAPI"}, {"name": "Deploy"}],
        "autor": {"name": "Pedro Martínez", "email": "pedro.martinez@devblog.com"},
        "created_at": "2024-02-18"
    },
    {
        "id": 5,
        "title": "Autenticación JWT en FastAPI: Implementación segura",
        "content": "Implementa autenticación stateless con JSON Web Tokens en tu API. Cubrimos OAuth2, passwords hashing con bcrypt, y cómo proteger rutas específicas usando dependencias de FastAPI.",
        "tags": [{"name": "Seguridad"}, {"name": "JWT"}, {"name": "FastAPI"}, {"name": "OAuth2"}],
        "autor": {"name": "Ana García", "email": "ana.garcia@devblog.com"},
        "created_at": "2024-03-01"
    },
    {
        "id": 6,
        "title": "SQLAlchemy 2.0 con FastAPI: Mejores prácticas",
        "content": "La nueva versión de SQLAlchemy trae cambios significativos. Descubre cómo configurar la nueva sintaxis de mapeo, usar AsyncSession para operaciones no bloqueantes y estructurar tu capa de datos mantenible.",
        "tags": [{"name": "SQLAlchemy"}, {"name": "Database"}, {"name": "FastAPI"}, {"name": "ORM"}],
        "autor": {"name": "Carlos Ruiz", "email": "carlos.ruiz@devblog.com"},
        "created_at": "2024-03-12"
    },
    {
        "id": 7,
        "title": "Testing en FastAPI: Pytest y TestClient",
        "content": "Escribir tests para APIs puede ser tedioso, pero FastAPI lo facilita. Aprende a usar TestClient, fixtures de Pytest, mocking de dependencias y cobertura de código para mantener tu aplicación libre de bugs.",
        "tags": [{"name": "Testing"}, {"name": "Pytest"}, {"name": "FastAPI"}, {"name": "TDD"}],
        "autor": {"name": "Laura Sánchez", "email": "laura.sanchez@devblog.com"},
        "created_at": "2024-03-25"
    },
    {
        "id": 8,
        "title": "WebSockets en FastAPI: Aplicaciones en tiempo real",
        "content": "Más allá de HTTP: implementa comunicación bidireccional con WebSockets. Construiremos un chat simple y explicaremos el manejo de conexiones, broadcast de mensajes y gestión de estado.",
        "tags": [{"name": "WebSockets"}, {"name": "Real-time"}, {"name": "FastAPI"}],
        "autor": {"name": "María López", "email": "maria.lopez@devblog.com"},
        "created_at": "2024-04-08"
    },
    {
        "id": 9,
        "title": "Optimización de performance en APIs Python",
        "content": "Tu API está lenta? Analizamos profiling con cProfile, caching con Redis, lazy loading de datos y técnicas de optimización de queries para reducir latencia y aumentar throughput.",
        "tags": [{"name": "Performance"}, {"name": "Redis"}, {"name": "Optimización"}, {"name": "Python"}],
        "autor": {"name": "Pedro Martínez", "email": "pedro.martinez@devblog.com"},
        "created_at": "2024-04-20"
    },
    {
        "id": 10,
        "title": "Documentación automática con OpenAPI y Swagger",
        "content": "Una de las killer features de FastAPI es la documentación automática. Profundizamos en cómo personalizar schemas, añadir ejemplos, describir errores y extender la UI de Swagger para tu equipo.",
        "tags": [{"name": "Documentación"}, {"name": "OpenAPI"}, {"name": "Swagger"}, {"name": "FastAPI"}],
        "autor": {"name": "Ana García", "email": "ana.garcia@devblog.com"},
        "created_at": "2024-05-05"
    },
    {
        "id": 11,
        "title": "Microservicios con FastAPI y comunicación entre servicios",
        "content": "Arquitectura de microservicios práctica: HTTP vs gRPC vs message queues. Implementamos service discovery, circuit breakers y tracing distribuido para sistemas resilientes.",
        "tags": [{"name": "Microservicios"}, {"name": "Arquitectura"}, {"name": "gRPC"}, {"name": "Distributed"}],
        "autor": {"name": "Carlos Ruiz", "email": "carlos.ruiz@devblog.com"},
        "created_at": "2024-05-18"
    },
    {
        "id": 12,
        "title": "Manejo de errores y excepciones personalizadas",
        "content": "No todas las excepciones deben devolver 500. Diseñamos handlers globales, excepciones de negocio personalizadas y respuestas de error consistentes siguiendo RFC 7807 (Problem Details).",
        "tags": [{"name": "Error Handling"}, {"name": "Best Practices"}, {"name": "FastAPI"}],
        "autor": {"name": "Laura Sánchez", "email": "laura.sanchez@devblog.com"},
        "created_at": "2024-06-01"
    }
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
                raise ValueError(f"El titulo no puede contener la palabra {word}")
        return value


class PostUpdate(BaseModel):
    title: Optional [str]
    content: Optional[str] = None #"Valor por defecto"


class PostPublic(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

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

class CommentBase(BaseModel):
    contenido: str = Field(
        ...,
        min_length=5,
        max_length=500
    )
    autor: str = Field(
        ...,
        min_length=3,
        max_length=50
    )


class CommentCreate(CommentBase):
    @field_validator("contenido")
    @classmethod
    def word_not_allowed(cls, value:str) -> str:
        for word in BANNED_WORDS:
            if word in value.lower():
                raise ValueError(f"La palabra {word} esta baneada")
        return value

class CommentPublic(CommentBase):
    id: int
    post_id: int
    created_at: str
    is_approved: bool


class CommentUpdate(BaseModel):
    contenido: Optional[str] = Field(
        ..., 
        min_length=5,
        max_length=500
    )
    
    @field_validator("contenido")
    @classmethod
    def word_not_allowed(cls, value: str | None) -> str | None:
        if value is None:
            return value
        for word in BANNED_WORDS:
            if word in value.lower():
                raise ValueError(f"La palabra {word} está baneada")
        return value
    
COMMENTS_DB = []
    
    
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


@app.post("/posts", response_model=PostPublic, response_description="Post creado (OK)", status_code=status.HTTP_201_CREATED)
#elipsis = ... significa que es obligatorio, None que es opcional
#post: dict= Body(...)
#Depends significa que depende de la funcion creada antes (def get_db())
def create_post(post: PostCreate, db: Session = Depends(get_db)):

    # if "title" not in post or "content" not in post:
    #     return {"error": "Title y content son requeridos"}
    # #.strip quita todos los espacios en blanco
    # if not str(post["title"]).strip():  
    #     return {"error": "Title no puede estar vacío"}
    #------------------------------------------------------
    # new_id= (BLOG_POST[-1]["id"]+1) if BLOG_POST else 1
    # new_post = {"id": new_id,
    #             "title": post.title,
    #             "content": post.content,
    #             "tags": [tag.model_dump() for tag in post.tags],
    #             "autor": post.autor.model_dump() if post.autor else None}#Esta forma de crear listas se conoce como list comprehension
    # BLOG_POST.append(new_post)
    # return new_post
    new_post = PostORM(title=post.title, content=post.content)
    try:
        db.add(new_post)
        db.commit()#para confirmar
        db.refresh(new_post)#actualizar objeto en memoria
        return new_post
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el post")

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



@app.post("/posts/{post_id}/comments", response_model=CommentPublic, response_description="Comentario creado")
def create_comment(post_id: int, comment: CommentCreate):
    for post in BLOG_POST:
        if post["id"] == post_id:
            new_id= (COMMENTS_DB[-1]["id"]+1) if COMMENTS_DB else 1
    
            new_comment = {
                "contenido": comment.contenido,
                "autor": comment.autor,
                "id": new_id,
                "post_id": post_id,
                "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
                "is_approved": False
            }
            COMMENTS_DB.append(new_comment)
            return new_comment
    raise HTTPException(status_code=404, detail="El post no existe")
    



#DOCUMENTACIONES AUTOMATICAS
#/docs
#/redoc