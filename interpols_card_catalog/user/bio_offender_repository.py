from dataclasses import dataclass
import sqlite3
from typing import List
from pypika import Query, Table


@dataclass
class BioCrimeEntity:
    id: str
    second_name: str
    name: str
    sex: str
    alias: str
    height: str
    hair_color: str
    eye_color: str
    special_features: str
    citizenship: str
    residence: str
    language: str
    place_of_birth: str
    date_of_birth: str
    criminal_profession: str
    last_crime: str
    status: str
    group_criminal: str


def execute_sql(query):
    connection = sqlite3.connect('database.sqlite')
    data = connection.execute(query)
    result = []
    for row in data:
        if row is None:
            break
        result.append(BioCrimeEntity(id=row[0],
                                     second_name=row[1],
                                     name=row[2],
                                     sex=row[3],
                                     alias=row[4],
                                     height=row[5],
                                     hair_color=row[6],
                                     eye_color=row[7],
                                     special_features=row[8],
                                     citizenship=row[9],
                                     residence=row[10],
                                     language=row[11],
                                     place_of_birth=row[12],
                                     date_of_birth=row[13],
                                     criminal_profession=row[14],
                                     last_crime=row[15],
                                     status=row[16], group_criminal=row[17]))
    connection.commit()
    connection.close()
    return result


class InmemoryBioCrimeRepository:
    def find_offender_by_id(self, bio_id) -> List[BioCrimeEntity]:
        select = execute_sql("select * from bio where id = '" + bio_id + "'")
        if len(select) == 0:
            return None
        return select

    def create_offender(self, offender: BioCrimeEntity):
        execute_sql("INSERT INTO bio (ID,SECOND_NAME,NAME,SEX,ALIAS,HEIGHT,\
            HAIR_COLOR,EYE_COLOR,SPECIAL_FEATURES,CITIZENSHIP,RESIDENCE,LANGUAGE,PLACE_OF_BIRTH,\
            DATE_OF_BIRTH, CRIMINAL_PROFESSION, LAST_CRIME, STATUS, GROUP_CRIMINAL) VALUES ('" + offender.id + "', '"
                    + offender.second_name + "', '"
                    + offender.name + "', '"
                    + offender.sex + "', '"
                    + offender.alias + "', '"
                    + offender.height + "', '"
                    + offender.hair_color + "', '"
                    + offender.eye_color + "', '"
                    + offender.special_features + "', '"
                    + offender.citizenship + "', '"
                    + offender.residence + "', '"
                    + offender.language + "', '"
                    + offender.place_of_birth + "', '"
                    + offender.date_of_birth + "', '"
                    + offender.criminal_profession + "', '"
                    + offender.last_crime + "', '"
                    + offender.status + "', '"
                    + offender.group_criminal + "')")

    def edit_offender(self, offender_id, offender: BioCrimeEntity):
        execute_sql(
            "UPDATE bio SET second_name = '" + offender.second_name + "' + name = '" + offender.name + "' + sex = '" +
            offender.sex + "' + alias = '" + offender.alias + "' + height = '" + offender.height + "' + hair_color = '" +
            offender.hair_color + "' + eye_color = '" + offender.eye_color + "' + special_features = '" +
            offender.special_features + "' + citizenship = '" + offender.citizenship + "' + language = '" +
            offender.language + "' + place_of_birth = '" + offender.place_of_birth + "' + date_of_birth = '" +
            offender.date_of_birth + "' + criminal_profession = '" + offender.criminal_profession + "' + last_crime = '" +
            offender.last_crime + "' + status = '" +
            offender.status + "' + group_criminal = '" + offender.group_criminal + "'WHERE id = '" + offender_id + "'")

    def find_all(self) -> [BioCrimeEntity]:
        return execute_sql("select * from bio WHERE status = 0")

    def find_all_archivers(self) -> [BioCrimeEntity]:
        return execute_sql("select * from bio WHERE status = 2")

    def find_offender_by_group(self, criminal_group) -> List[BioCrimeEntity]:
        select = execute_sql("select * from bio WHERE group_criminal = '" + criminal_group + "'")
        if len(select) == 0:
            return None
        return select

    def delete_by_id(self, bio_id):
        execute_sql("UPDATE bio SET status = 1 WHERE status = 0 AND id = '" + bio_id + "'")

    def archive_by_id(self, bio_id):
        execute_sql("UPDATE bio SET status = 2 WHERE status = 0 AND id = '" + bio_id + "'")

    def count(self):
        return len(self.find_all())

    def filter_by_parameters(self, arguments_of_filtration):
        bio = Table('bio')
        q = Query.from_(bio).select("*")

        for key in arguments_of_filtration:
            value = arguments_of_filtration[key]
            q = q.where(
                bio[key] == value
            )
        return execute_sql(str(q))
