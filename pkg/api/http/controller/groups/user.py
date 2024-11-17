import quart
import sqlalchemy

from .. import group
from .....persistence.entities import user


@group.group_class('user', '/api/v1/user')
class UserRouterGroup(group.RouterGroup):
    
    async def initialize(self) -> None:
        @self.route('/init', methods=['GET', 'POST'], auth_type=group.AuthType.NONE)
        async def _() -> str:
            if quart.request.method == 'GET':
                return self.success(data={
                    'initialized': await self.ap.user_service.is_initialized()
                })
            
            if await self.ap.user_service.is_initialized():
                return self.fail(1, '系统已初始化')

            json_data = await quart.request.json

            user_email = json_data['user']
            password = json_data['password']

            await self.ap.user_service.create_user(user_email, password)

            return self.success()
        
        @self.route('/auth', methods=['POST'], auth_type=group.AuthType.NONE)
        async def _() -> str:
            json_data = await quart.request.json

            token = await self.ap.user_service.authenticate(json_data['user'], json_data['password'])

            return self.success(data={
                'token': token
            })

        @self.route('/check-token', methods=['GET'])
        async def _() -> str:
            return self.success()