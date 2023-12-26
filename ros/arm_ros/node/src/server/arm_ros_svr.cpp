#include <stdio.h>
#include "arm_ros.h"

using namespace arm_ros;

#define PORT 2468

//----
bool ArmROS_svr::init()
{
    Arm::addCreator("ros", 
        []()->Sp<Arm>{ return mkSp<ArmROS>();  });
    return true;
}
//-----
static bool run_arm_ros_svr()
{

    ros::AsyncSpinner spinner(1);
    spinner.start();
    
    ArmROS_svr svr;
    if(!svr.init())
        return false;

    //---
    string s = "arm_ros_server node started...";
    s += "CurDir:"+ sys::pwd();
    ut::log_i(s);
    //----
    svr.run_server(PORT);
    //----

    return true;
}
//------------
// main
//------------
int main(int argc, char **argv)
{
    using namespace std;
    ros::init(argc, argv, "arm_ros_test");
    run_arm_ros_svr();
    
    return 0;
}
