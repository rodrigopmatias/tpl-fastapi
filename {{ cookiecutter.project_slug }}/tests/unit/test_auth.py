import pytest
from {{cookiecutter.project_module}}.auth import User


class TestUser:
    @pytest.mark.parametrize("role", ("role1", "role2", "role3"))
    def test_allowed_when_is_admin(self, role: str):
        user = User(id=1, email="fake@mail.com", is_admin=True, roles=[])
        assert user.allowed(role) == True

    @pytest.mark.parametrize("role", ("role1", "role2", "role3"))
    def test_allowed_when_role_is_not_allowed(self, role: str) -> None:
        user = User(
            id=1,
            email="fake@mail.com",
            is_admin=False,
            roles=["xrole1", "xrole2", "xrole3", "xrole4"],
        )
        assert user.allowed(role) == False

    @pytest.mark.parametrize("role", ("role1", "role2", "role3"))
    def test_allowed_when_role_allowed(self, role: str) -> None:
        user = User(
            id=1,
            email="fake@mail.com",
            is_admin=False,
            roles=["role1", "role2", "role3", "role4"],
        )
        assert user.allowed(role) == True
