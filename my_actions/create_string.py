from aijson import register_action

class Inputs(BaseModel):
    string: str

class Outputs(BaseModel):
    string: str

class LoadJSON(Action[Inputs, Outputs]):
    name = "create_string"
    async def run(self, inputs: Inputs) -> Outputs:
        print(inputs.string)
        return Outputs(string=inputs.string)

