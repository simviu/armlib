#include <stdio.h>
#include "arm_ros.h"

using namespace arm_ros;

bool ArmROS::init()
{
    log_i("ArmROS init MoveIt...");    

    p_arm_ = moveit::planning_interface::MoveGroupInterface(cfg_.sGroup);
    auto& arm = * p_arm_;
    arm.allowReplanning(true);
    arm.setPoseReferenceFrame("g_base");
    arm.setGoalPositionTolerance(cfg_.goalToler.pos);
    arm.setGoalOrientationTolerance(cfg_.goalToler.orien);
    arm.setMaxVelocityScalingFactor(cfg_.max_spd_scl);
    log_i("  init MoveIt done");    

    return true;
}
//-----
bool ArmROS::setJoints(const ArmSt& st, double t)
{

    std::vector<double> arm_joint_positions = {0.9, -1.4, -0.7, 0.8, -0.5, -0.6};
    vector<double> js;
    for(auto& j : st.angles)
        js.push_back(toRad(j));
    arm.setJointValueTarget(js);
    arm.move();
    return true;
}
//----
bool ArmROS::moveTo(const TipSt& ts, float spd=1.0)
{
    if(p_arm_ == nullptr) {
        log_e("ArmROS not init")
        return false;
    }
    //-----
    arm.setStartStateToCurrentState();
    log_i("  moving to p ...");

    //-----
    string sFrm = arm.getPlanningFrame();
    geometry_msgs::PoseStamped p; 
    //----
    p.header.frame_id = sFrm;
    p.header.stamp = ros::Time::now();
    p.pose.position = st.pos;
    p.pose.orientation.x = 0.026;
    p.pose.orientation.y = 1.0;
    p.pose.orientation.z = 0.0;
    p.pose.orientation.w = 0.014;


    arm.setPoseTarget(p);

    return true;

}
//-----
bool ArmROS::getSt(ArmSt& st)
{
    return true;

}
