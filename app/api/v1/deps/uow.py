from app.utils.unit_of_work import UnitOfWork

def uow_factory() -> UnitOfWork:
    return UnitOfWork()