from dependency_injector import containers, providers

from marketplace.settings import settings
from marketplace.infrastructure.db import engine, SessionLocal


class BaseContainer(containers.DeclarativeContainer):
    """
    - settings: current app config
    - db_engine: AsyncEngine
    - db_session_factory: async_sessionmaker
    """

    wiring_config = containers.WiringConfiguration()

    config = providers.Object(settings)

    db_engine = providers.Object(engine)
    db_session_factory = providers.Object(SessionLocal)
