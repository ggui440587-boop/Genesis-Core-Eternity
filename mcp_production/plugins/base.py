class BasePlugin:
    async def execute(self):
        raise NotImplementedError("所有插件必須實作 execute 方法")

