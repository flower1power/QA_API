from enum import Enum

import requests
from faker import Faker

faker = Faker()


class CharacterStatus(Enum):
    Alive = "Alive"
    Dead = "Dead"
    Unknown = "unknown"


def get_all_character() -> None:
    """
    Получение всех персонажей Рик и Морти
    """
    base_url = 'https://rickandmortyapi.com/api/character'
    page = 1
    total_page = 1

    while page <= total_page:
        response = requests.get(
            url=base_url,
            params={'page': str(page)}
        )
        assert response.status_code == 200
        json_response = response.json()
        characters = json_response["results"]
        total_page = json_response["info"]['pages']

        for character in characters:
            name = character['name']
            print(name)

        page = page + 1


def find_characters_by_name(character_name: str) -> None:
    """
    Получение всех персонажей Рик и Морти по имени
    Args:
        character_name: str - имя персонажа
    """
    response = requests.get(url='https://rickandmortyapi.com/api/character', params={'name': character_name})
    assert response.status_code == 200
    json = response.json()
    characters = json["results"]
    count = len(characters)
    print('\ncharacters_count:', count)


def get_characters_by_status(status: CharacterStatus):
    """
    Получение всех персонажей Рик и Морти по имени
    Args:
        status:(CharacterStatus) - статус персонажа
    """
    base_url = 'https://rickandmortyapi.com/api/character'
    page = 1
    total_page = 1

    while page != total_page:
        response = requests.get(
            url=base_url,
            params={'page': str(page + 1), 'status': status.value}
        )
        assert response.status_code == 200

        json_response = response.json()
        total_page = json_response["info"]['pages']
        characters = json_response["results"]

        for character in characters:
            assert character['status'] == status.value
            print(character)

        page = page + 1


def create_user(name: str, job: str) -> str:
    """
    Создание user
    Args:
        name: str - user name
        job: str - user job

    Returns:
        id: str user id
    """
    response = requests.post(url='https://reqres.in/api/users', headers={
        'x-api-key': 'reqres-free-v1'
    }, json={
        "name": name,
        "job": job
    })

    assert response.status_code == 201
    print(response.json())

    return response.json()['id']


def update_user_job(user_id: str, new_job: str) -> None:
    """
    Изменение профессии user по id
    Args:
        user_id: str - user id
        new_job: str - user new job
    """
    response = requests.patch(url=f'https://reqres.in/api/users/{user_id}', headers={
        'x-api-key': 'reqres-free-v1'
    }, json={
        "job": new_job
    })

    assert response.status_code == 200
    response_json = response.json()
    assert response_json['job'] == new_job
    print(response_json)


def delete_user(user_id) -> None:
    """
    Удаление user по id
    Args:
        user_id: str - user id
    """
    response = requests.delete(url=f'https://reqres.in/api/users/{user_id}', headers={
        'x-api-key': 'reqres-free-v1'
    })

    assert response.status_code == 204
    print(response)


get_all_character()
find_characters_by_name(character_name='rick')
get_characters_by_status(CharacterStatus.Unknown)

created_user_id = create_user(name=faker.name(), job='qa')
update_user_job(user_id=created_user_id, new_job='aqa')
delete_user(user_id=created_user_id)
