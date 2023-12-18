#pragma once

#include "vsn/vsnLib.h"
#include "arm/armLib.h"

#include "ros/ros.h"
#include "std_msgs/String.h"

namespace arm_ros{
    using namespace std;
    using namespace ut;
    using namespace arm;
    //---------

    //---------
    class ArmRosTest{
    public:
        void run();
    protected:
        ros::NodeHandle nh_;
        bool test_arm_joints();
        bool test_arm_pose();
    };
}
