from json import loads

def compareLists(self, dbList, testList):
    for i, dbSkill in enumerate(dbList):
        if type(testList) is not list:
            testSkill = loads(testList)[i]
        else:
            testSkill = testList[i]
        self.assertEquals(testSkill, dbSkill)



def compareDicts(self, dbDict, testDict):
    testDict['VacancyId'] = dbDict['VacancyId']
    testDict['UserId'] = self.userId
    testDict['IsOpen'] = True
    
    del dbDict['Created']

    return self.assertDictEqual(dbDict, testDict)