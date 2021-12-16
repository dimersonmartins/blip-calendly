import requests
import json
import uuid


class Widget:
    def __init__(self, authorizationKey, telefone, calendly='', nome='', conta='', assessor='', codAssessor='', email=''):
        self.authorizationKey = authorizationKey
        self.telefone = telefone
        self.identity = telefone+"@wa.gw.msging.net"
        self.email = email
        self.conta = conta
        self.nome = nome
        self.assessor = assessor
        self.codAssessor = codAssessor
        self.calendly = calendly

    def Guid(self):
        return str(uuid.uuid4())

    async def UpdateOrCreate(self):
        response = await self.GetAccount()
        data = response.json()
        extras = {}
        if('success' in data['status']):
            extras = self.Update(data)
        else:
            extras = self.Create()

        return await self.SetAccount(extras)

    async def GetAccount(self):
        data = {
            "id": self.Guid(),
            "method": "get",
            "uri": "/contacts/"+self.identity,
        }

        return await self.send(data)

    async def SetAccount(self, resource):
        data = {
            "id": self.Guid(),
            "method": "set",
            "uri": "/contacts",
            "type": "application/vnd.lime.contact+json",
            "resource": resource
        }

        return await self.send(data)

    def Update(self, data):
        resource = data['resource']
        if 'extras' in resource:
            extras = resource['extras']
            if(not extras):
                return self.Create()
            else:
                if (self.nome):
                    resource['name'] = self.nome
                if (self.email):
                    resource['email'] = self.email
                if (self.telefone):
                    resource['phoneNumber'] = self.telefone

                for child in extras:
                    if ('Calendly' in child and self.calendly):
                        extras['Calendly'] = self.calendly
                    elif(self.calendly):
                        extras = self.CreateProp(
                            extras, 'Calendly', self.calendly)

                    if ('Conta' in child and self.conta):
                        extras['Conta'] = self.conta
                    elif(self.conta):
                        extras = self.CreateProp(
                            extras, 'Conta', self.conta)

                    if ('Assessor' in child and self.assessor):
                        extras['Assessor'] = self.assessor
                    elif(self.assessor):
                        extras = self.CreateProp(
                            extras, 'Assessor', self.assessor)

                    if ('CodAssessor' in child and self.codAssessor):
                        extras['CodAssessor'] = self.codAssessor
                    elif(self.codAssessor):
                        extras = self.CreateProp(
                            extras, 'CodAssessor', self.codAssessor)

                    resource['extras'] = extras
                    return resource
        else:
            return self.Create()

    def CreateProp(self, data, prop, value):
        data[prop] = value
        return data

    def Create(self):
        resource = {}
        extras = {}

        if (self.identity):
            resource['identity'] = self.identity

        if (self.email):
            resource['email'] = self.email

        if (self.nome):
            resource['name'] = self.nome

        if (self.telefone):
            resource['phoneNumber'] = self.telefone

        if (self.calendly):
            extras['Calendly'] = self.calendly

        if (self.conta):
            extras['Conta'] = self.conta

        if (self.assessor):
            extras['Assessor'] = self.assessor

        if (self.codAssessor):
            extras['CodAssessor'] = self.codAssessor

        resource = resource['extras'] = extras
        return resource

    async def send(self, data):
        jsonData = json.dumps(data)
        return requests.post('https://http.msging.net/commands', data=jsonData, headers={'Content-Type': 'application/json',
                                                                                         'Authorization': self.authorizationKey})
