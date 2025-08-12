from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Depends, HTTPException, status

from marketplace.products.schemas.product_dto import (
    ProductDTO,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from marketplace.products.container import ProductsContainer
from marketplace.products.services.product_service import ProductService


router = APIRouter(prefix="/products", tags=["products"])


# TODO: return errors in a better way (from service)

@router.post("", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
@inject
async def create_product(
    payload: ProductCreateSchema,
    service: ProductService = Depends(Provide[ProductsContainer.product_service]),
) -> ProductDTO:
    try:
        return await service.create_product(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    

@router.get("/{id}", response_model=ProductDTO)
@inject
async def get_product_by_id(
    id: UUID,
    service: ProductService = Depends(Provide[ProductsContainer.product_service]),
) -> ProductDTO:
    try:
        return await service.get_product_by_id(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("", response_model=List[ProductDTO])
@inject
async def get_all_products(
    limit: int = 20,
    offset: int = 0,
    service: ProductService = Depends(Provide[ProductsContainer.product_service]),
) -> List[ProductDTO]:
    try:
        return await service.get_all_products(limit, offset)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/{id}", response_model=ProductDTO)
@inject
async def update_product(
    id: UUID,
    payload: ProductUpdateSchema,
    service: ProductService = Depends(Provide[ProductsContainer.product_service]),
) -> ProductDTO:
    try:
        return await service.update_product(id, payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_product(
    id: UUID,
    service: ProductService = Depends(Provide[ProductsContainer.product_service]),
) -> None:
    try:
        await service.delete_product(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
