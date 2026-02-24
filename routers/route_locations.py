from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.models.country import Country
from database.session import get_db

from database.repository.crud_location import get_countries, get_country_by_id, create_country, update_country, \
    delete_country
from database.repository.provinces import get_provinces
from database.repository.cities import get_cities_by_province

from routers.route_login import get_current_user
from schemas.Schema_Country import CountryRead, CountryCreate, CountryUpdate
from schemas.Schema_Location import LocationRead, LocationCreate, LocationUpdate

router = APIRouter()


@router.get('/provinces', summary="دریافت لیست تمام استان‌ها", status_code=status.HTTP_200_OK)
def list_provinces(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        provinces = get_provinces(db)
        if not provinces:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No provinces found"
            )
        return {p.id: p.name for p in provinces}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/cities/', summary="دریافت لیست شهرهای یک استان با شناسه استان (province_id)", status_code=status.HTTP_200_OK)
def list_cities(province_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        cities = get_cities_by_province(db, province_id)
        if not cities:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No cities found for this province"
            )
        return {c.id: c.name for c in cities}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/countries/', summary="دریافت لیست کشور ها", status_code=status.HTTP_200_OK)
def list_countries(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        countries = get_countries(db)

        if not countries:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No countries found"
            )

        return {country.id: country.title for country in countries}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching countries: {str(e)}")


@router.get('/{country_id}', response_model=CountryRead)
def get_country(country_id: int,
                current_user: str = Depends(get_current_user),
                db: Session = Depends(get_db)):

    country = get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    return country

@router.post('/countries/', response_model=CountryRead, status_code=status.HTTP_201_CREATED)
def add_country(data: CountryCreate,
                current_user: str = Depends(get_current_user),
                db: Session = Depends(get_db)):

    existing = db.query(Country).filter(Country.title == data.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Country already exists")

    return create_country(db, data)

@router.put('/countries/{country_id}', response_model=CountryRead)
def edit_country(country_id: int,
                 data: CountryUpdate,
                 current_user: str = Depends(get_current_user),
                 db: Session = Depends(get_db)):

    country = get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    return update_country(db, country, data)


# حذف کشور
@router.delete('/countries/{country_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_country(country_id: int,
                   current_user: str = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    country = get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    delete_country(db, country)

# @router.post("/", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
# def create_location(location: LocationCreate, db: Session = Depends(get_db)):
#     return location_crud.create_location(db, location)
#
#
# @router.get("/", response_model=list[LocationRead])
# def get_locations(db: Session = Depends(get_db)):
#     return location_crud.get_all_locations(db)
#
#
# @router.get("/{location_id}", response_model=LocationRead)
# def get_location(location_id: int, db: Session = Depends(get_db)):
#     db_location = location_crud.get_location(db, location_id)
#
#     if not db_location:
#         raise HTTPException(status_code=404, detail="Location یافت نشد")
#
#     return db_location
#
#
# @router.put("/{location_id}", response_model=LocationRead)
# def update_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
#     db_location = location_crud.get_location(db, location_id)
#
#     if not db_location:
#         raise HTTPException(status_code=404, detail="Location یافت نشد")
#
#     return location_crud.update_location(db, db_location, location)
#
#
# @router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_location(location_id: int, db: Session = Depends(get_db)):
#     db_location = location_crud.get_location(db, location_id)
#
#     if not db_location:
#         raise HTTPException(status_code=404, detail="Location یافت نشد")
#
#     location_crud.delete_location(db, db_location)