from Uav import *

class Groups:

    def init_group(self,uav_count):
        self.uav_count = uav_count
        self.group = []
        self.groups = []
        for i in range(self.uav_count):
            self.group.append(i)
        
        self.groups.append(self.group)
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
        

    def AppendGroups(self,second,first):

        if first == second :
            return

        new_group = self.groups[second]

        for i in new_group:
            self.groups[first].append(i)

        self.groups[first].sort()

        new_group = self.groups.pop(second)
        i = 0
        for group in self.groups:
            for uav in group:
                uavList[uav].info["Grup"] = i
            i += 1

        print(self.groups)

        
groups = Groups()
