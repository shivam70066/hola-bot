from configs.database_connection import prisma_connection

class UserDataServices:
    @staticmethod
    async def saveUserdata(src:str,userID : int, ids:list):
        return await prisma_connection.prisma.userdata.create({
            "source":src,
            "userId":userID,
            "datachunks":ids
        })
        
    @staticmethod
    async def getSources(userID:int):
        userdata= await prisma_connection.prisma.userdata.find_many(
            where={
                "userId":userID
            }
        )
        sources = []
        for data in userdata:
        # Assuming data.id is a hashable type (e.g., int, str)
            sources.append({
            "source_name": data.source,
            "source_id": data.id
            })

        return sources
    
    @staticmethod
    async def getSourceChunksIds(userId : int, srcId:str):
        sourceData= await prisma_connection.prisma.userdata.find_many(
            where={
                "id": srcId
            }
        )
        datachunks= None
        for data in sourceData:
            datachunks = data.datachunks
        return datachunks
    
    @staticmethod
    async def deleteSource(srcId:str):
        isDeleted = await prisma_connection.prisma.userdata.delete(
            where={
                'id': srcId
            }
        )
        if isDeleted is None:
            return False
        
        return True