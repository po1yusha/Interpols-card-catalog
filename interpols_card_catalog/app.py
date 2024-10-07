from flask import Flask
from user.user_repository import InmemoryUserRepository
from user.login_controller import init as init_login_controller
from user.user_controller import init as init_user_controller
from user.user_service import UserService
from login_filter import init as init_login_filter
from session_filter import init as init_session_filter

from user.bio_offender_repository import InmemoryBioCrimeRepository
from user.offender_controller import init as init_offender_controller
from user.offender_service import OffenderService

app = Flask(__name__)
repository = InmemoryUserRepository()
service = UserService(repository)
repository_offender = InmemoryBioCrimeRepository()
service_offender = OffenderService(repository_offender)
# init_user_controller(app, service)
init_offender_controller(app, service_offender, service)
init_login_controller(app, service)
init_login_filter(app)
init_session_filter(app)



