from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.session import get_db

from database.repository.country import get_countries
from database.repository.provinces import get_provinces
from database.repository.cities import get_cities_by_province

from routers.route_login import get_current_user


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