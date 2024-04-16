from prisma import Prisma

class PrismaConnection: 
    
    def __init__(self):
        self.prisma = Prisma()
        
    async def connect(self):
        print("Prisma connected")
        await self.prisma.connect()
        
    async def disconnect(self):
        print("Prisma disconnected")
        await self.prisma.disconnect()
        
prisma_connection = PrismaConnection()