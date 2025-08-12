from dependency_injector import containers, providers

from marketplace.containers.base import BaseContainer
from marketplace.products.container import ProductsContainer


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            # "marketplace.products",
            # "marketplace.users",
        ],
    )

    base = providers.Container(BaseContainer)

    products = providers.Container(
        ProductsContainer,
        db_session_factory=base.db_session_factory,
    )
