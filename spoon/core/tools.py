class BaseTool:
    name: str
    description: str
    parameters: dict

    async def execute(self, *args, **kwargs):
        raise NotImplementedError
