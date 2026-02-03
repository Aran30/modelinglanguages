import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Comment", "description": "Operations for Comment entities"},
        {"name": "Comment Relationships", "description": "Manage Comment relationships"},
        {"name": "BlogPost", "description": "Operations for BlogPost entities"},
        {"name": "BlogPost Relationships", "description": "Manage BlogPost relationships"},
        {"name": "BlogPost Methods", "description": "Execute BlogPost methods"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")
    
    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error", 
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["comment_count"] = database.query(Comment).count()
    stats["blogpost_count"] = database.query(BlogPost).count()
    stats["total_entities"] = sum(stats.values())
    return stats

############################################
#
#   Comment functions
#
############################################
 
 

@app.get("/comment/", response_model=None, tags=["Comment"])
def get_all_comment(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload
    
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Comment)
        query = query.options(joinedload(Comment.blogpost))
        comment_list = query.all()
        
        # Serialize with relationships included
        result = []
        for comment_item in comment_list:
            item_dict = comment_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)
            
            # Add many-to-one relationships (foreign keys for lookup columns)
            if comment_item.blogpost:
                related_obj = comment_item.blogpost
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['blogpost'] = related_dict
            else:
                item_dict['blogpost'] = None
            
            
            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Comment).all()


@app.get("/comment/count/", response_model=None, tags=["Comment"])
def get_count_comment(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Comment entities"""
    count = database.query(Comment).count()
    return {"count": count}


@app.get("/comment/paginated/", response_model=None, tags=["Comment"])
def get_paginated_comment(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Comment entities"""
    total = database.query(Comment).count()
    comment_list = database.query(Comment).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": comment_list
    }


@app.get("/comment/search/", response_model=None, tags=["Comment"])
def search_comment(
    database: Session = Depends(get_db)
) -> list:
    """Search Comment entities by attributes"""
    query = database.query(Comment)
    
    
    results = query.all()
    return results


@app.get("/comment/{comment_id}/", response_model=None, tags=["Comment"])
async def get_comment(comment_id: int, database: Session = Depends(get_db)) -> Comment:
    db_comment = database.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    response_data = {
        "comment": db_comment,
}
    return response_data



@app.post("/comment/", response_model=None, tags=["Comment"])
async def create_comment(comment_data: CommentCreate, database: Session = Depends(get_db)) -> Comment:

    if comment_data.blogpost is not None:
        db_blogpost = database.query(BlogPost).filter(BlogPost.id == comment_data.blogpost).first()
        if not db_blogpost:
            raise HTTPException(status_code=400, detail="BlogPost not found")
    else:
        raise HTTPException(status_code=400, detail="BlogPost ID is required")

    db_comment = Comment(
        timestamp=comment_data.timestamp,        content=comment_data.content,        authorName=comment_data.authorName,        blogpost_id=comment_data.blogpost        )

    database.add(db_comment)
    database.commit()
    database.refresh(db_comment)



    
    return db_comment


@app.post("/comment/bulk/", response_model=None, tags=["Comment"])
async def bulk_create_comment(items: list[CommentCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Comment entities at once"""
    created_items = []
    errors = []
    
    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.blogpost:
                raise ValueError("BlogPost ID is required")
            
            db_comment = Comment(
                timestamp=item_data.timestamp,                content=item_data.content,                authorName=item_data.authorName,                blogpost_id=item_data.blogpost            )
            database.add(db_comment)
            database.flush()  # Get ID without committing
            created_items.append(db_comment.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})
    
    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})
    
    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Comment entities"
    }


@app.delete("/comment/bulk/", response_model=None, tags=["Comment"])
async def bulk_delete_comment(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Comment entities at once"""
    deleted_count = 0
    not_found = []
    
    for item_id in ids:
        db_comment = database.query(Comment).filter(Comment.id == item_id).first()
        if db_comment:
            database.delete(db_comment)
            deleted_count += 1
        else:
            not_found.append(item_id)
    
    database.commit()
    
    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Comment entities"
    }

@app.put("/comment/{comment_id}/", response_model=None, tags=["Comment"])
async def update_comment(comment_id: int, comment_data: CommentCreate, database: Session = Depends(get_db)) -> Comment:
    db_comment = database.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    setattr(db_comment, 'timestamp', comment_data.timestamp)
    setattr(db_comment, 'content', comment_data.content)
    setattr(db_comment, 'authorName', comment_data.authorName)
    if comment_data.blogpost is not None:
        db_blogpost = database.query(BlogPost).filter(BlogPost.id == comment_data.blogpost).first()
        if not db_blogpost:
            raise HTTPException(status_code=400, detail="BlogPost not found")
        setattr(db_comment, 'blogpost_id', comment_data.blogpost)
    database.commit()
    database.refresh(db_comment)
    
    return db_comment


@app.delete("/comment/{comment_id}/", response_model=None, tags=["Comment"])
async def delete_comment(comment_id: int, database: Session = Depends(get_db)):
    db_comment = database.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    database.delete(db_comment)
    database.commit()
    return db_comment





############################################
#
#   BlogPost functions
#
############################################
 
 

@app.get("/blogpost/", response_model=None, tags=["BlogPost"])
def get_all_blogpost(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload
    
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(BlogPost)
        blogpost_list = query.all()
        
        # Serialize with relationships included
        result = []
        for blogpost_item in blogpost_list:
            item_dict = blogpost_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)
            
            # Add many-to-one relationships (foreign keys for lookup columns)
            
            # Add many-to-many and one-to-many relationship objects (full details)
            comment_list = database.query(Comment).filter(Comment.blogpost_id == blogpost_item.id).all()
            item_dict['hasComments'] = []
            for comment_obj in comment_list:
                comment_dict = comment_obj.__dict__.copy()
                comment_dict.pop('_sa_instance_state', None)
                item_dict['hasComments'].append(comment_dict)
            
            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(BlogPost).all()


@app.get("/blogpost/count/", response_model=None, tags=["BlogPost"])
def get_count_blogpost(database: Session = Depends(get_db)) -> dict:
    """Get the total count of BlogPost entities"""
    count = database.query(BlogPost).count()
    return {"count": count}


@app.get("/blogpost/paginated/", response_model=None, tags=["BlogPost"])
def get_paginated_blogpost(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of BlogPost entities"""
    total = database.query(BlogPost).count()
    blogpost_list = database.query(BlogPost).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": blogpost_list
        }
    
    result = []
    for blogpost_item in blogpost_list:
        hasComments_ids = database.query(Comment.id).filter(Comment.blogpost_id == blogpost_item.id).all()
        item_data = {
            "blogpost": blogpost_item,
            "hasComments_ids": [x[0] for x in hasComments_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/blogpost/search/", response_model=None, tags=["BlogPost"])
def search_blogpost(
    database: Session = Depends(get_db)
) -> list:
    """Search BlogPost entities by attributes"""
    query = database.query(BlogPost)
    
    
    results = query.all()
    return results


@app.get("/blogpost/{blogpost_id}/", response_model=None, tags=["BlogPost"])
async def get_blogpost(blogpost_id: int, database: Session = Depends(get_db)) -> BlogPost:
    db_blogpost = database.query(BlogPost).filter(BlogPost.id == blogpost_id).first()
    if db_blogpost is None:
        raise HTTPException(status_code=404, detail="BlogPost not found")

    hasComments_ids = database.query(Comment.id).filter(Comment.blogpost_id == db_blogpost.id).all()
    response_data = {
        "blogpost": db_blogpost,
        "hasComments_ids": [x[0] for x in hasComments_ids]}
    return response_data



@app.post("/blogpost/", response_model=None, tags=["BlogPost"])
async def create_blogpost(blogpost_data: BlogPostCreate, database: Session = Depends(get_db)) -> BlogPost:


    db_blogpost = BlogPost(
        image=blogpost_data.image,        content=blogpost_data.content,        title=blogpost_data.title,        timestamp=blogpost_data.timestamp,        authorName=blogpost_data.authorName        )

    database.add(db_blogpost)
    database.commit()
    database.refresh(db_blogpost)

    if blogpost_data.hasComments:
        # Validate that all Comment IDs exist
        for comment_id in blogpost_data.hasComments:
            db_comment = database.query(Comment).filter(Comment.id == comment_id).first()
            if not db_comment:
                raise HTTPException(status_code=400, detail=f"Comment with id {comment_id} not found")
        
        # Update the related entities with the new foreign key
        database.query(Comment).filter(Comment.id.in_(blogpost_data.hasComments)).update(
            {Comment.blogpost_id: db_blogpost.id}, synchronize_session=False
        )
        database.commit()


    
    hasComments_ids = database.query(Comment.id).filter(Comment.blogpost_id == db_blogpost.id).all()
    response_data = {
        "blogpost": db_blogpost,
        "hasComments_ids": [x[0] for x in hasComments_ids]    }
    return response_data


@app.post("/blogpost/bulk/", response_model=None, tags=["BlogPost"])
async def bulk_create_blogpost(items: list[BlogPostCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple BlogPost entities at once"""
    created_items = []
    errors = []
    
    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            
            db_blogpost = BlogPost(
                image=item_data.image,                content=item_data.content,                title=item_data.title,                timestamp=item_data.timestamp,                authorName=item_data.authorName            )
            database.add(db_blogpost)
            database.flush()  # Get ID without committing
            created_items.append(db_blogpost.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})
    
    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})
    
    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} BlogPost entities"
    }


@app.delete("/blogpost/bulk/", response_model=None, tags=["BlogPost"])
async def bulk_delete_blogpost(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple BlogPost entities at once"""
    deleted_count = 0
    not_found = []
    
    for item_id in ids:
        db_blogpost = database.query(BlogPost).filter(BlogPost.id == item_id).first()
        if db_blogpost:
            database.delete(db_blogpost)
            deleted_count += 1
        else:
            not_found.append(item_id)
    
    database.commit()
    
    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} BlogPost entities"
    }

@app.put("/blogpost/{blogpost_id}/", response_model=None, tags=["BlogPost"])
async def update_blogpost(blogpost_id: int, blogpost_data: BlogPostCreate, database: Session = Depends(get_db)) -> BlogPost:
    db_blogpost = database.query(BlogPost).filter(BlogPost.id == blogpost_id).first()
    if db_blogpost is None:
        raise HTTPException(status_code=404, detail="BlogPost not found")

    setattr(db_blogpost, 'image', blogpost_data.image)
    setattr(db_blogpost, 'content', blogpost_data.content)
    setattr(db_blogpost, 'title', blogpost_data.title)
    setattr(db_blogpost, 'timestamp', blogpost_data.timestamp)
    setattr(db_blogpost, 'authorName', blogpost_data.authorName)
    if blogpost_data.hasComments is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Comment).filter(Comment.blogpost_id == db_blogpost.id).update(
            {Comment.blogpost_id: None}, synchronize_session=False
        )
        
        # Set new relationships if list is not empty
        if blogpost_data.hasComments:
            # Validate that all IDs exist
            for comment_id in blogpost_data.hasComments:
                db_comment = database.query(Comment).filter(Comment.id == comment_id).first()
                if not db_comment:
                    raise HTTPException(status_code=400, detail=f"Comment with id {comment_id} not found")
            
            # Update the related entities with the new foreign key
            database.query(Comment).filter(Comment.id.in_(blogpost_data.hasComments)).update(
                {Comment.blogpost_id: db_blogpost.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_blogpost)
    
    hasComments_ids = database.query(Comment.id).filter(Comment.blogpost_id == db_blogpost.id).all()
    response_data = {
        "blogpost": db_blogpost,
        "hasComments_ids": [x[0] for x in hasComments_ids]    }
    return response_data


@app.delete("/blogpost/{blogpost_id}/", response_model=None, tags=["BlogPost"])
async def delete_blogpost(blogpost_id: int, database: Session = Depends(get_db)):
    db_blogpost = database.query(BlogPost).filter(BlogPost.id == blogpost_id).first()
    if db_blogpost is None:
        raise HTTPException(status_code=404, detail="BlogPost not found")
    database.delete(db_blogpost)
    database.commit()
    return db_blogpost



############################################
#   BlogPost Method Endpoints
############################################


@app.post("/blogpost/methods/addComment/", response_model=None, tags=["BlogPost Methods"])
async def blogpost_addComment(
    database: Session = Depends(get_db)
):
    """
    Execute the addComment class method on BlogPost.
    This method operates on all BlogPost entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the class method
        result = BlogPost.addComment(database)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}
        
        return {
            "class": "BlogPost",
            "method": "addComment",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



