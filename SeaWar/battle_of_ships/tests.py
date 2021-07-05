from django.test import TestCase
import pytest
from rest_framework.test import APIRequestFactory

# Create your tests here.
from battle_of_ships.shortcart import Ship


@pytest.fixture
def ship_1():
    ship = Ship(coordinates=[], hit_coordinates=['A1'])
    return ship


@pytest.fixture
def ship_2():
    ship = Ship(coordinates=['A1', 'H7'], hit_coordinates=['A1', 'H7'])
    return ship


@pytest.fixture
def ship_3():
    ship = Ship(coordinates=['A1', 'H7', "k5"], hit_coordinates=['A1'])
    return ship


@pytest.fixture
def harbor(ship_1, ship_2, ship_3):
    return [ship_1, ship_2, ship_3]


@pytest.mark.parametrize('position, hit_coordinate, faire, result', [
    (['A1'], [], 'A1', 'killed'),
    (['A1', 'H7'], ['A1'], 'K5', 'mimo'),
    (['A1', 'H7', "k5"], ['A1'], 'K5', 'ranen')
    ])
def test_check_hit(position, hit_coordinate, faire, result):
    assert Ship(coordinates=position, hit_coordinates=faire).check_hit(coordinate=faire)


def test_killed(ship_2, ship_3):
    assert ship_2.coordinates == ['A1', 'H7']
    assert ship_2.hit_coordinates == ['A1', 'H7']
    assert ship_2.killed()
    assert ship_3.killed() == False
