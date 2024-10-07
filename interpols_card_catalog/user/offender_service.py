from typing import List
from user.bio_offender_repository import BioCrimeEntity, InmemoryBioCrimeRepository


class LastOffenderException(Exception):
    pass


class ExistOffenderException(Exception):
    pass


class OffenderService:
    def __init__(self, bio_offender_repository: InmemoryBioCrimeRepository):
        self.bio_offender_repository = bio_offender_repository

    def get_all_offenders(self) -> [BioCrimeEntity]:
        return self.bio_offender_repository.find_all()

    def get_offenders_with_filter(self, arguments_of_filtration):
        args = {}
        for key in arguments_of_filtration:
            value = arguments_of_filtration[key]
            if value is not None and value != "":
                args[key] = value
        return self.bio_offender_repository.filter_by_parameters(args)

    def get_all_archive_offenders(self) -> [BioCrimeEntity]:
        return self.bio_offender_repository.find_all_archivers()

    def delete_offender(self, bio_id: str):
        if self.bio_offender_repository.count() <= 1:
            raise LastOffenderException("Cannot remove last offender")
        self.bio_offender_repository.delete_by_id(bio_id)

    def archive_offender(self, bio_id: str):
        self.bio_offender_repository.archive_by_id(bio_id)

    def add_offender(self, bio_id: str, offender: BioCrimeEntity):
        if self.bio_offender_repository.find_offender_by_id(bio_id) is not None:
            raise ExistOffenderException("Offender already exists")
        self.bio_offender_repository.create_offender(offender)

    def edit_offender(self, offender_id: str, offender: BioCrimeEntity):
        self.bio_offender_repository.edit_offender(offender_id, offender)

    def get_offender_by_id(self, bio_id) -> List[BioCrimeEntity]:
        return self.bio_offender_repository.find_offender_by_id(bio_id)

    def get_group_offenders(self, criminal_group) -> List[BioCrimeEntity]:
        return self.bio_offender_repository.find_offender_by_group(criminal_group)
