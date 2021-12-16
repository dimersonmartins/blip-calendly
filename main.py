import asyncio
import widget as Take


async def ContatoBlip():
    widget = Take.Widget(authorizationKey='Key',
                         telefone='5511999999999',
                         calendly="https://calendly.com/pt",
                         nome="Nome do usuário",
                         conta="123456",
                         assessor="Nome do Assessor",
                         codAssessor="45",
                         email="email@example.com")

    await widget.UpdateOrCreate()


asyncio.run(ContatoBlip())
