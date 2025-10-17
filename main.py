from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import database
import models
from database import PersonDB

app = FastAPI(
    title="Genealogy Tree API",
    description="API for genealogy tree (PostgreSQL)",
    version="1"
    )

async def get_person(db: AsyncSession, person_id: int) -> PersonDB:
    result = await db.execute(select(PersonDB).filter(PersonDB.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

async def get_person_FN(db: AsyncSession, first_name: str) -> PersonDB:
    result = await db.execute(select(PersonDB).filter(PersonDB.first_name == first_name))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

async def build_ancestor_tree(db: AsyncSession, person_id: int, depth: Optional[int] = None, current_depth: int = 0) -> Optional[dict]:
    if depth is not None and current_depth >= depth:
       return None
    
    person = await get_person(db, person_id)
    
    result = {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "mother": None,
        "father": None
        }
    
    if person.mother_id:
        result["mother"] = await build_ancestor_tree(db, person.mother_id, depth, current_depth + 1)
    
    if person.father_id:
        result["father"] = await build_ancestor_tree(db, person.father_id, depth, current_depth + 1)
    
    return result

@app.get("/v1/people", response_model=List[models.Person])
async def get_people(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(database.get_db)
    ):
    result = await db.execute(select(PersonDB).offset(skip).limit(limit))
    people = result.scalars().all()
    return people

@app.post("/v1/people", response_model=models.Person)
async def create_person(
    person: models.PersonCreate,
    db: AsyncSession = Depends(database.get_db)
    ):
    
    if person.mother_id:
        result = await db.execute(select(PersonDB).filter(PersonDB.id == person.mother_id))
        mother = result.scalar_one_or_none()
        if not mother:
            raise HTTPException(status_code=400, detail="Mother not found")
    
    if person.father_id:
        result = await db.execute(select(PersonDB).filter(PersonDB.id == person.father_id))
        father = result.scalar_one_or_none()
        if not father:
            raise HTTPException(status_code=400, detail="Father not found")
    
    db_person = PersonDB(
        first_name=person.first_name,
        last_name=person.last_name,
        mother_id=person.mother_id,
        father_id=person.father_id
    )
    
    db.add(db_person)
    try:
        await db.commit()
        await db.refresh(db_person)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Person with this first name already exists")
    return db_person

@app.get("/v1/people/{person_id}", response_model=models.Person)
async def get_person_by_id(
    person_id: int,
    db: AsyncSession = Depends(database.get_db)
    ):

    return await get_person(db, person_id)

@app.get("/v1/people/name/{first_name}", response_model=models.Person_FN)
async def get_person_by_first_name(
    first_name: str,
    db: AsyncSession = Depends(database.get_db)
    ):

    return await get_person_FN(db, first_name)

@app.put("/v1/people/{person_id}", response_model=models.Person)
async def update_person(
    person_id: int,
    person_update: models.PersonUpdate,
    db: AsyncSession = Depends(database.get_db)
    ):
    db_person = await get_person(db, person_id)
    
    if person_update.mother_id is not None:
        if person_update.mother_id != db_person.mother_id:
            result = await db.execute(select(PersonDB).filter(PersonDB.id == person_update.mother_id))
            mother = result.scalar_one_or_none()
            if not mother:
                raise HTTPException(status_code=400, detail="Mother not found")
    
    if person_update.father_id is not None:
        if person_update.father_id != db_person.father_id:
            result = await db.execute(select(PersonDB).filter(PersonDB.id == person_update.father_id))
            father = result.scalar_one_or_none()
            if not father:
                raise HTTPException(status_code=400, detail="Father not found")
    
    update_data = person_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_person, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_person)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Person with this first name already exists")
    return db_person

@app.get("/v1/people/{person_id}/ancestors")
async def get_ancestors_by_id(
    person_id: int,
    depth: Optional[int] = Query(None, ge=1, description="Depth"),
    db: AsyncSession = Depends(database.get_db)
    ):
    person = await get_person(db, person_id)
    
    result = {}
    
    if person.mother_id:
        result["mother"] = await build_ancestor_tree(db, person.mother_id, depth, 0)
    
    if person.father_id:
        result["father"] = await build_ancestor_tree(db, person.father_id, depth, 0)
    
    return result

@app.get("/v1/people/name/{first_name}/ancestors")
async def get_ancestors_by_name(
    first_name: str,
    depth: Optional[int] = Query(None, ge=1, description="Depth"),
    db: AsyncSession = Depends(database.get_db)
    ):
    person = await get_person_FN(db, first_name)
    
    result = {}
    
    if person.mother_id:
        result["mother"] = await build_ancestor_tree(db, person.mother_id, depth, 0)
    
    if person.father_id:
        result["father"] = await build_ancestor_tree(db, person.father_id, depth, 0)
    
    return result

@app.get("/check")
async def check():
    return {"status": "working"}