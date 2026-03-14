from backend.app.services.user_service import UserService
from backend.app.models.user import User

def test_create_user_success(session):
    """
    GIVEN valid user data
    WHEN the create_user method is called
    THEN a new user should be created in the database with a hashed password
    """
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    user, msg = UserService.create_user(user_data)

    assert user is not None
    assert user.username == 'testuser'
    assert user.id is not None
    assert user.password_hash != 'password123'
    assert user.check_password('password123')
    assert msg == "User created successfully."

def test_create_user_duplicate_username(session):
    """
    GIVEN a user already exists in the database
    WHEN the create_user method is called with the same username
    THEN it should not create a new user and should return an error message
    """
    # First, create a user
    user_data1 = {'username': 'testuser', 'email': 'test1@example.com', 'password': 'password123'}
    UserService.create_user(user_data1)

    # Now, try to create another with the same username
    user_data2 = {'username': 'testuser', 'email': 'test2@example.com', 'password': 'password456'}
    user, msg = UserService.create_user(user_data2)

    assert user is None
    assert msg == "A user with this username or email already exists."

def test_get_user_by_id(session):
    """
    GIVEN a user exists in the database
    WHEN the get_user_by_id method is called with the user's id
    THEN it should return the correct user object
    """
    user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}
    created_user, _ = UserService.create_user(user_data)

    retrieved_user = UserService.get_user_by_id(created_user.id)

    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == 'testuser'

def test_update_user(session):
    """
    GIVEN a user exists in the database
    WHEN the update_user method is called with new data
    THEN the user's details should be updated
    """
    user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}
    user, _ = UserService.create_user(user_data)

    update_data = {'username': 'updateduser', 'role': 'admin'}
    updated_user, msg = UserService.update_user(user.id, update_data)

    assert updated_user is not None
    assert updated_user.username == 'updateduser'
    assert updated_user.role == 'admin'
    assert msg == "User updated successfully."

def test_delete_user(session):
    """
    GIVEN a user exists in the database
    WHEN the delete_user method is called
    THEN the user should be removed from the database
    """
    user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}
    user, _ = UserService.create_user(user_data)

    success, msg = UserService.delete_user(user.id)

    assert success is True
    assert msg == "User deleted successfully."
    assert UserService.get_user_by_id(user.id) is None


#
# VesselService Tests
#

from backend.app.services.vessel_service import VesselService
from backend.app.models.vessel import Vessel

def test_create_vessel_success(session):
    """
    GIVEN valid vessel data
    WHEN the create_vessel method is called
    THEN a new vessel should be created
    """
    # Create an owner first
    owner_data = {'username': 'owner', 'email': 'owner@sea.com', 'password': 'password'}
    owner, _ = UserService.create_user(owner_data)

    vessel_data = {
        'mmsi': '123456789',
        'name': 'The Salty Squid',
        'vessel_type': 'Trawler',
        'length_m': 25.5,
        'beam_m': 6.2
    }
    vessel, msg = VesselService.create_vessel(vessel_data, owner_id=owner.id)

    assert vessel is not None
    assert vessel.name == 'The Salty Squid'
    assert vessel.mmsi == '123456789'
    assert vessel.owner_id == owner.id
    assert msg == "Vessel created successfully."

def test_create_vessel_duplicate_mmsi(session):
    """
    GIVEN a vessel with a specific MMSI already exists
    WHEN trying to create another vessel with the same MMSI
    THEN it should fail and return an error message
    """
    vessel_data = {'mmsi': '111222333', 'name': 'The重複'}
    VesselService.create_vessel(vessel_data)

    vessel2_data = {'mmsi': '111222333', 'name': 'The Sequel'}
    vessel, msg = VesselService.create_vessel(vessel2_data)

    assert vessel is None
    assert msg == "A vessel with this MMSI already exists."

def test_update_vessel(session):
    """
    GIVEN an existing vessel
    WHEN the update_vessel method is called with new data
    THEN the vessel's details should be updated
    """
    vessel_data = {'mmsi': '987654321', 'name': 'Old Name'}
    vessel, _ = VesselService.create_vessel(vessel_data)

    update_data = {'name': 'New Name', 'vessel_type': 'Longliner'}
    updated_vessel, msg = VesselService.update_vessel(vessel.id, update_data)

    assert updated_vessel is not None
    assert updated_vessel.name == 'New Name'
    assert updated_vessel.vessel_type == 'Longliner'
    assert msg == "Vessel updated successfully."

def test_delete_vessel(session):
    """
    GIVEN an existing vessel
    WHEN the delete_vessel method is called
    THEN the vessel should be removed from the database
    """
    vessel_data = {'mmsi': '555555555', 'name': 'Goner'}
    vessel, _ = VesselService.create_vessel(vessel_data)

    success, msg = VesselService.delete_vessel(vessel.id)

    assert success is True
    assert msg == "Vessel deleted successfully."
    assert VesselService.get_vessel_by_id(vessel.id) is None
