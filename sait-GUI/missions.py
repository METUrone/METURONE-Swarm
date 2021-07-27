
class Swarm:
    def __init__(self,ID,x,y,z,batarya):
        self.ID = ID
        self.x = x
        self.y = y
        self.z = z
        self.batarya = batarya
        self.aktif = "Hayır"
        self.group = 0

    def getList(self):
        a = []
        a.append(str(self.ID))
        a.append(str(self.aktif))
        a.append(str(self.x))
        a.append(str(self.y))
        a.append(str(self.z))
        a.append(str(self.batarya))
        a.append(str(self.group))
        return a

class Vec3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class SetFormation:
    def __init__(self,x,y,z , formationSide , distance , group):
        self.Center = Vec3(x,y,z)
        self.formationSide = formationSide
        self.distance = distance
        self.group = group

class SetHareket:
    def __init__(self,x,y,z,group):
        self.Hedef = Vec3(x,y,z)
        self.group = group

class Groups:
    def __init__(self,swarmcount):
        group = []
        for i in range(swarmcount):
            group.append(i)
        self.groups = []
        self.groups.append(group)

    def SplitGroup(self,first,swarms):

        if len(swarms) == 0:
            return
        new_group = []
        for i in swarms:
            self.groups[first].remove(i)
            new_group.append(i)
        self.groups.append(new_group)
        if len(self.groups[first]) == 0:
            self.groups.pop(first)

    def AppendGroups(self,first,second):

        if first == second :
            return

        new_group = self.groups[second]

        for i in new_group:
            self.groups[first].append(i)

        self.groups[first].sort()

        new_group = self.groups.pop(second)

        