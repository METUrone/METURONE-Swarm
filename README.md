# METURONE-Swarm

`METURONE-Swarm` is a decentralized controller for homogeneous multi-agent systems. With `METURONE-Swarm`, you can control up to 12(it is tested with 12 agents, if you test it with more agents, please let us know!) agents in an obstacle-free environment. Current features are formation constructing, trajectory following, rotating the swarm around its center and dividing the group into any number of groups, each with a different mission.

# How to Install?
First, clone the repository.
```shell
git clone https://github.com/METUrone/METURONE-Swarm.git
```
Then install the required packages with
```shell
pip3 install requirements.txt
```
That's it! However, if you will use ROS to communicate with your robots, you also need to install ROS from https://wiki.ros.org/ROS/Installation.

# How to use?
Although the system allows using with any kind of agent, current code only supports Crazyflie agents with OptiTrack systems. To adapt it to your system, you should rewrite `poses.py`, getting the position and orientation information somehow and print it. We are aware that this is not performance-friendly, and will change it soon. There are also Crazyflie-specific code in `commander.py`, you may need to change them or delete them according to your needs. 

You may also implement a different algorithm very easily with `METURONE-Swarm`. The only thing you should do is implementing `calculate_speed` and `CalculateCollisionSpeed` functions in `uav.py`. 

After you adapt the system to your agents, you only run below command.
```shell
python3 gui3.py
```
![Screenshot from 2021-12-20 01-46-21](https://user-images.githubusercontent.com/41516584/146693627-4f016412-d800-482b-8dee-90d365671d9e.png)

In the interface you can watch the agents from the left panel and right below panel, and give commands from the right top panel on-the-fly or before the mission.
![Screenshot from 2021-12-20 01-46-18](https://user-images.githubusercontent.com/41516584/146693635-8a67a6ca-519f-441f-8cc5-0fbee06fcfac.png)


# Want to Contribute?
Feel free to open issues and pull requests, and you can also read our report for this project [METURONE-Swarm.pdf](https://github.com/METUrone/METURONE-Swarm/files/7741726/METURONE-Swarm.pdf). However, it is only in Turkish for now.
