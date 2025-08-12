from dependency_injector import containers, providers

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from marketplace.products.repositories.product_repository import ProductRepository
from marketplace.products.services.product_service import ProductService


class ProductsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "marketplace.products.api.routes",
        ],
    )

    db_session_factory = providers.Dependency(instance_of=async_sessionmaker)

    product_repository = providers.Singleton(
        ProductRepository,
        session_factory=db_session_factory,
    )

    product_service = providers.Singleton(
        ProductService,
        repository=product_repository,
    )
