#pragma once

#include "arm_ros.h"

//---------
namespace arm_ros{
    class ArmRosTest{
    public:
        void run();
    protected:
        ros::NodeHandle nh_;
        bool test_moveit_joints();
        bool test_moveit_pose();
        
    };
}
