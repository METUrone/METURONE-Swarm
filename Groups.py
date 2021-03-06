from Uav import *

class Groups:

    def __init__(self):

        self.groups = []
        self.formation_info = {}
    def init_group(self,uav_count):
        self.uav_count = uav_count
        self.group = []
        for i in range(self.uav_count):
            self.group.append(i)

        self.SetFormationInfos(0,"Yok" , "Yok")
        

        self.groups.append(self.group)

    def GetCenter(self , group):
        return [self.formation_info[group][2],self.formation_info[group][3],self.formation_info[group][4]]

    def SetCenter(self, group,center):
        self.formation_info[group][2] = center[0]
        self.formation_info[group][3] = center[1]
        self.formation_info[group][4] = center[2]

    def SetFormationInfos(self,group,formation,center,x = 0.0,y = 0.0,z = 0.0):

        self.formation_info[group] = [formation,center,x,y,z]

    def RemoveUav(self,group,uav):
        self.groups[group].remove(uav)
        if self.groups[group] == []:
            self.DelFormationInfo(group)


    def DelFormationInfo(self,group):
        del self.formation_info[group] 
        self.groups.pop(group)

    def SplitGroup(self,first,uavs):


        if len(uavs) == 0 :
            return

        if len(self.groups[first])==1:
            return
        new_group = []
        for i in uavs:
            self.groups[first].remove(i)
            new_group.append(i)
            uavList[i].info["Grup"] = len(self.groups)

        
        
        self.groups.append(new_group)
        self.SetFormationInfos(len(self.groups)-1,"Yok","Yok")

    def AppendGroups(self,second,first):

        if first == second :
            return

        new_group = self.groups[second]

        for i in new_group:
            self.groups[first].append(i)

        self.SetFormationInfos(first,"Yok","Yok")
        self.SetFormationInfos(second,"Yok","Yok")

        self.groups[first].sort()

        new_group = self.groups.pop(second)

        
        i = 0
        for group in self.groups:
            for uav in group:
                uavList[uav].info["Grup"] = i
            i += 1

        

        
groups = Groups()


