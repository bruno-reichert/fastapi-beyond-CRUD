from src.auth.schemas import UserCreateModel
from src.auth import routes
from src import celery_tasks
from unittest.mock import AsyncMock, patch, MagicMock

auth_prefix = "/api/v1/auth"

def test_user_creation(fake_session, fake_user_service, test_client):
    signup_data = {
        "username": "TestMan123",
        "email": "testman@ascaes.com",
        "password": "testing123!!",
        "first_name": "Aperture Science",
        "last_name": "User Creation Test Fake User"
    }
    
    # Create a mock user object to return from create_user
    mock_user = MagicMock()
    mock_user.email = signup_data["email"]
    
    # Mock the async service methods
    fake_user_service.user_exists = AsyncMock(return_value=False)
    fake_user_service.create_user = AsyncMock(return_value=mock_user)
    
    # Patch both the user_service and the celery task
    with patch.object(routes, 'user_service', fake_user_service), \
         patch.object(celery_tasks, 'send_email') as mock_send_email:
        mock_send_email.delay = MagicMock()
        response = test_client.post(
            url=f"{auth_prefix}/signup",
            json=signup_data
        )

    user_data = UserCreateModel(**signup_data)

    # Use actual Mock assertion methods
    fake_user_service.user_exists.assert_called_once_with(signup_data['email'], fake_session)
    fake_user_service.create_user.assert_called_once_with(user_data, fake_session)