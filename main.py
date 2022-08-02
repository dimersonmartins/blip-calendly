import asyncio
import widget as Take
import pandas as pd

colunas = ['Telefone', 'Nome', 'Conta', 'Calendly', 'Assessor', 'CodAssessor', 'Email']

df = pd.read_csv('disparo2_cr_2903.csv',
                 skipinitialspace=True, usecols=colunas)

async def ContatoBlip():
    for index, row in df.iterrows():
        widget = Take.Widget(authorizationKey='Key aqui', #Chave do Bot Router
                             telefone=row.Telefone,
                             nome=row.Nome,
                             conta=row.Conta,
                             calendly=row.Calendly,
                             assessor=row.Assessor,
                             codAssessor=row.CodAssessor,
                             email=row.Email) 
        

        await widget.UpdateOrCreate()


asyncio.run(ContatoBlip())
